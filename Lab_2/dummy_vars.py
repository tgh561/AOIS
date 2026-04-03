def get_dummy_vars(table, vars_list):
    n = len(vars_list)
    dummies = []
    for i in range(n):
        is_dummy = True
        bit = 1 << i
        for mask in range(1 << n):
            if (mask & bit) == 0:
                if table[mask] != table[mask | bit]:
                    is_dummy = False
                    break
        if is_dummy:
            dummies.append(vars_list[i])
    return dummies