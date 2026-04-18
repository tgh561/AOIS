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
