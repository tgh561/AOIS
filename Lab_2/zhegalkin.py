def get_zhegalkin(table, vars_list):
    n = len(vars_list)
    A = table[:]
    for i in range(n):
        for mask in range(1 << n):
            if mask & (1 << i):
                A[mask] ^= A[mask ^ (1 << i)]
    terms = []
    for mask in range(1 << n):
        if A[mask]:
            if mask == 0:
                terms.append("1")
            else:
                term = "".join(vars_list[j] for j in range(n) if mask & (1 << j))
                terms.append(term)
    return " ⊕ ".join(terms) or "0"