def _gray_order(bits):
    return [i ^ (i >> 1) for i in range(1 << bits)]


def _mask_from_row_col(rv, cv, nrow, ncol):
    m = 0
    for i in range(nrow):
        if (rv >> i) & 1:
            m |= 1 << i
    for j in range(ncol):
        if (cv >> j) & 1:
            m |= 1 << (nrow + j)
    return m


def _mask_karnaugh_5(rv, cv, e_val, nrow_bits, ncol_bits, e_index):
    m = (e_val & 1) << e_index
    for i in range(nrow_bits):
        if (rv >> i) & 1:
            m |= 1 << i
    for j in range(ncol_bits):
        if (cv >> j) & 1:
            m |= 1 << (nrow_bits + j)
    return m


def _print_submap(table, vars_list, nrow_bits, ncol_bits, g_row, g_col, e_val, title):
    row_vars = "".join(vars_list[:nrow_bits])
    col_vars = "".join(vars_list[nrow_bits : nrow_bits + ncol_bits])
    col_headers = [format(x, f"0{ncol_bits}b") for x in g_col]
    e_index = len(vars_list) - 1
    print(f"   {title}")
    print(f"   {row_vars} \\ {col_vars}")
    print("      " + " ".join(col_headers))
    for rv in g_row:
        row_label = format(rv, f"0{nrow_bits}b") if nrow_bits else ""
        cells = []
        for cv in g_col:
            idx = _mask_karnaugh_5(rv, cv, e_val, nrow_bits, ncol_bits, e_index)
            cells.append(str(table[idx]))
        print(f"   {row_label}  " + " ".join(cells))


def print_karnaugh_map(table, vars_list, caption=None):
    if caption:
        print(f"   {caption}")
    n = len(vars_list)
    if n == 0:
        print("   f =", table[0])
        return

    if n == 1:
        v0 = vars_list[0]
        print(f"   {v0}")
        g = _gray_order(1)
        line = "  ".join(str(table[x]) for x in g)
        print("  " + line)
        return

    if n == 5:
        nrow_bits = 2
        ncol_bits = 2
        split_var = vars_list[4]
        g_row = _gray_order(nrow_bits)
        g_col = _gray_order(ncol_bits)
        _print_submap(
            table,
            vars_list,
            nrow_bits,
            ncol_bits,
            g_row,
            g_col,
            0,
            f"{split_var} = 0",
        )
        print()
        _print_submap(
            table,
            vars_list,
            nrow_bits,
            ncol_bits,
            g_row,
            g_col,
            1,
            f"{split_var} = 1",
        )
        return

    nrow_bits = n // 2
    ncol_bits = n - nrow_bits
    row_vars = "".join(vars_list[:nrow_bits])
    col_vars = "".join(vars_list[nrow_bits:])
    g_row = _gray_order(nrow_bits)
    g_col = _gray_order(ncol_bits)

    col_headers = [format(x, f"0{ncol_bits}b") for x in g_col]
    label = f"{row_vars} \\ {col_vars}"
    print(f"   {label}")
    print("      " + " ".join(col_headers))
    for rv in g_row:
        row_label = format(rv, f"0{nrow_bits}b") if nrow_bits else ""
        cells = []
        for cv in g_col:
            idx = _mask_from_row_col(rv, cv, nrow_bits, ncol_bits)
            cells.append(str(table[idx]))
        print(f"   {row_label}  " + " ".join(cells))


def _cube_bits(cube, n):
    value, care = cube
    out = []
    for i in range(n - 1, -1, -1):
        if (care >> i) & 1:
            out.append("1" if (value >> i) & 1 else "0")
        else:
            out.append("X")
    return "".join(out)


def _all_cubes(n):
    cubes = []
    total = 3**n
    for code in range(total):
        v = code
        value = 0
        care = 0
        for i in range(n):
            d = v % 3
            v //= 3
            if d == 0:
                care |= 1 << i
            elif d == 1:
                care |= 1 << i
                value |= 1 << i
        cubes.append((value, care))
    return cubes


def _cube_covers(cube, m):
    value, care = cube
    return (m & care) == (value & care)


def _cube_to_dnf_term(cube, vars_list):
    value, care = cube
    parts = []
    for i, var in enumerate(vars_list):
        if not ((care >> i) & 1):
            continue
        parts.append(var if ((value >> i) & 1) else f"!{var}")
    return " & ".join(parts) if parts else "1"


def _cube_to_cnf_clause(cube, vars_list):
    value, care = cube
    parts = []
    for i, var in enumerate(vars_list):
        if not ((care >> i) & 1):
            continue
        parts.append(f"!{var}" if ((value >> i) & 1) else var)
    return "(" + " | ".join(parts) + ")" if parts else "(?)"


def _literal_count(cube):
    _, care = cube
    return care.bit_count()


def _choose_cover(primes, cover_sets, target):
    target = set(target)
    if not target:
        return []

    inv = {m: [] for m in target}
    for i, s in enumerate(cover_sets):
        for m in s:
            if m in inv:
                inv[m].append(i)

    chosen = set()
    unresolved = set(target)
    changed = True
    while changed:
        changed = False
        for m in list(unresolved):
            cand = [i for i in inv[m] if i not in chosen]
            if len(cand) == 1:
                i = cand[0]
                chosen.add(i)
                unresolved -= cover_sets[i]
                changed = True

    remaining = sorted([i for i in range(len(primes)) if i not in chosen], key=lambda x: (_literal_count(primes[x]), x))
    best = None

    def dfs(pos, covered, picked):
        nonlocal best
        if unresolved <= covered:
            sol = list(chosen) + picked
            key = (len(sol), sum(_literal_count(primes[i]) for i in sol))
            if best is None or key < best[0]:
                best = (key, sol[:])
            return
        if pos >= len(remaining):
            return
        if best is not None and len(chosen) + len(picked) >= best[0][0]:
            return

        i = remaining[pos]
        dfs(pos + 1, covered | cover_sets[i], picked + [i])
        dfs(pos + 1, covered, picked)

    dfs(0, set(), [])
    if best is None:
        return sorted(chosen)
    return sorted(best[1])


def karnaugh_minimize(table, vars_list, form="dnf", show_groups=True):
    n = len(vars_list)
    label = "ДНФ" if form == "dnf" else "КНФ"
    work = table if form == "dnf" else [1 - x for x in table]
    ones = {i for i, v in enumerate(work) if v}

    if not ones:
        print(f"   Минимальная {label}:", "0" if form == "dnf" else "1")
        return
    if len(ones) == (1 << n):
        print(f"   Минимальная {label}:", "1" if form == "dnf" else "0")
        return

    valid = []
    for cube in _all_cubes(n):
        cov = {m for m in range(1 << n) if _cube_covers(cube, m)}
        if not cov:
            continue
        if cov <= ones:
            valid.append((cube, cov))

    primes = []
    for i, (c1, s1) in enumerate(valid):
        is_prime = True
        for j, (c2, s2) in enumerate(valid):
            if i != j and s1 < s2:
                is_prime = False
                break
        if is_prime:
            primes.append((c1, s1))

    prime_cubes = [p[0] for p in primes]
    cover_sets = [p[1] for p in primes]
    pick = _choose_cover(prime_cubes, cover_sets, ones)
    picked_cubes = [prime_cubes[i] for i in pick]

    if show_groups:
        print("   Группы карты Карно:")
        for c in picked_cubes:
            print("     ", _cube_bits(c, n))

    if form == "dnf":
        terms = [_cube_to_dnf_term(c, vars_list) for c in picked_cubes]
        print(f"   Минимальная {label}:", " | ".join(terms))
    else:
        clauses = [_cube_to_cnf_clause(c, vars_list) for c in picked_cubes]
        print(f"   Минимальная {label}:", " & ".join(clauses))
