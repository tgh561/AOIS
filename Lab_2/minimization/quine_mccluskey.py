from collections import defaultdict


def _merge_two(c1, c2):
    v1, m1 = c1
    v2, m2 = c2
    if m1 != m2:
        return None
    diff = (v1 ^ v2) & m1
    if diff == 0 or (diff & (diff - 1)) != 0:
        return None
    nm = m1 & ~diff
    nv = v1 & nm
    return (nv, nm)


def _ones_count(cube):
    v, care = cube
    return (v & care).bit_count()


def _merge_pass(cubes):
    cubes = list(cubes)
    by_ones = defaultdict(list)
    for c in cubes:
        by_ones[_ones_count(c)].append(c)
    new_cubes = set()
    used = set()
    keys = sorted(by_ones.keys())
    for k in keys:
        if k + 1 not in by_ones:
            continue
        for c1 in by_ones[k]:
            for c2 in by_ones[k + 1]:
                m = _merge_two(c1, c2)
                if m is not None:
                    new_cubes.add(m)
                    used.add(c1)
                    used.add(c2)
    primes = {c for c in cubes if c not in used}
    return new_cubes, primes


def _prime_implicants(minterms, n, show_stages):
    current = {(m, (1 << n) - 1) for m in minterms}
    all_primes = set()
    stage = 0
    while current:
        if show_stages:
            print(f"   Этап склеивания {stage}:")
            for c in sorted(current, key=lambda x: (_ones_count(x), x[0])):
                print("     ", _cube_bits(c, n))
        nxt, finished = _merge_pass(current)
        all_primes |= finished
        if not nxt:
            break
        current = nxt
        stage += 1
    return all_primes


def _cube_bits(cube, n):
    v, care = cube
    s = []
    for i in range(n - 1, -1, -1):
        if (care >> i) & 1:
            s.append("1" if (v >> i) & 1 else "0")
        else:
            s.append("X")
    return "".join(s)


def _cube_to_dnf_term(cube, vars_list):
    v, care = cube
    n = len(vars_list)
    parts = []
    for i in range(n):
        if not ((care >> i) & 1):
            continue
        if (v >> i) & 1:
            parts.append(vars_list[i])
        else:
            parts.append(f"~{vars_list[i]}")
    return " & ".join(parts) if parts else "1"


def _covers(cube, minterm, n):
    v, care = cube
    return (minterm & care) == (v & care)


def _build_chart(minterms, primes, n):
    prime_list = sorted(primes, key=lambda c: (_ones_count(c), c[0]))
    rows = {m: [] for m in minterms}
    for j, p in enumerate(prime_list):
        for m in minterms:
            if _covers(p, m, n):
                rows[m].append(j)
    return prime_list, rows


def _minimal_cover(minterms, prime_list, rows):
    if not minterms:
        return []
    uncovered = set(minterms)
    cover_idx = []
    while uncovered:
        essential_j = None
        for m in uncovered:
            cand = [j for j in rows[m] if j not in cover_idx]
            if len(cand) == 1:
                essential_j = cand[0]
                break
        if essential_j is not None:
            cover_idx.append(essential_j)
            uncovered = {m for m in uncovered if essential_j not in rows[m]}
            continue
        best_j = None
        best_cov = None
        best_key = None
        for j in range(len(prime_list)):
            if j in cover_idx:
                continue
            cov = {m for m in uncovered if j in rows[m]}
            if not cov:
                continue
            key = (-len(cov), j)
            if best_key is None or key < best_key:
                best_key = key
                best_j = j
                best_cov = cov
        if best_j is None:
            break
        cover_idx.append(best_j)
        uncovered -= best_cov
    return cover_idx


def _remove_redundant(cover_idx, prime_list, minterms, n):
    cover_idx = list(cover_idx)
    changed = True
    while changed:
        changed = False
        for j in list(cover_idx):
            rest = [prime_list[k] for k in cover_idx if k != j]
            ok = True
            for m in minterms:
                if not any(_covers(p, m, n) for p in rest):
                    ok = False
                    break
            if ok:
                cover_idx.remove(j)
                changed = True
                break
    return cover_idx


def _print_pi_table(minterms, prime_list, n, vars_list):
    print("   Таблица покрытия (конституэнты × импликанты):")
    header = "м/п".ljust(6)
    for j, p in enumerate(prime_list):
        header += str(j + 1).center(4)
    print(header)
    for m in sorted(minterms):
        row = str(m).ljust(6)
        for j, p in enumerate(prime_list):
            row += (" X " if _covers(p, m, n) else "   ").center(4)
        print(row)
    print("   Импликанты:", ", ".join(f"{j+1}:{_cube_to_dnf_term(p, vars_list)}" for j, p in enumerate(prime_list)))


def quine_mccluskey_minimize(table, vars_list, show_stages=True, method="calc"):
    n = len(vars_list)
    minterms = [i for i, v in enumerate(table) if v]
    if not minterms:
        print("   0 (постоянный 0)")
        return
    if len(minterms) == 1 << n:
        print("   1 (постоянная 1)")
        return

    primes = _prime_implicants(set(minterms), n, show_stages)
    prime_list, rows = _build_chart(minterms, primes, n)
    cover_idx = _minimal_cover(minterms, prime_list, rows)
    cover_idx = _remove_redundant(cover_idx, prime_list, minterms, n)

    if method == "table" and show_stages:
        _print_pi_table(minterms, prime_list, n, vars_list)

    terms = [_cube_to_dnf_term(prime_list[j], vars_list) for j in sorted(cover_idx)]
    result = " | ".join(terms)
    print("   Минимальная ДНФ:", result)
