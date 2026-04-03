from itertools import combinations


def print_derivatives(table, vars_list):
    n = len(vars_list)
    max_order = min(4, n)
    print("\nБулевы производные (частные и смешанные, порядок 1–%d):" % max_order)
    for k in range(1, max_order + 1):
        for idxs in combinations(range(n), k):
            der = _derivative(table, list(idxs))
            name = _derivative_label(vars_list, idxs)
            print(f"  {name} = {_format_derivative(der)}")


def _derivative_label(vars_list, idxs):
    if len(idxs) == 1:
        return f"∂f/∂{vars_list[idxs[0]]}"
    syms = "".join(f"∂{vars_list[i]}" for i in idxs)
    return f"∂^{len(idxs)}f/({syms})"


def _format_derivative(der):
    n = len(der).bit_length() - 1
    parts = []
    for mask in range(1 << n):
        if der[mask]:
            bits = [str((mask >> i) & 1) for i in range(n)]
            parts.append("(" + ",".join(bits) + ")")
    return "1 на наборах: " + ", ".join(parts) if parts else "0"


def _derivative(table, var_indices):
    n = len(table).bit_length() - 1
    k = len(var_indices)
    bitmask = sum(1 << idx for idx in var_indices)
    der = [0] * (1 << n)
    for base in range(1 << n):
        if base & bitmask:
            continue
        xor_val = 0
        for sub in range(1 << k):
            flip = sum((1 << var_indices[b]) for b in range(k) if (sub & (1 << b)))
            xor_val ^= table[base | flip]
        for sub in range(1 << k):
            flip = sum((1 << var_indices[b]) for b in range(k) if (sub & (1 << b)))
            der[base | flip] = xor_val
    return der
