def _mobius_anf(table, n):
    a = table[:]
    for i in range(n):
        for mask in range(1 << n):
            if mask & (1 << i):
                a[mask] ^= a[mask ^ (1 << i)]
    return a


def _is_linear_anf(a, n):
    for mask in range(1 << n):
        if a[mask] and mask.bit_count() > 1:
            return False
    return True


def get_post_classes(table, n):
    classes = []
    if table[0] == 0:
        classes.append("T0")
    if table[(1 << n) - 1] == 1:
        classes.append("T1")
    mono = True
    for a in range(1 << n):
        for b in range(a + 1, 1 << n):
            if (a & b) == a and table[a] > table[b]:
                mono = False
                break
        if not mono:
            break
    if mono:
        classes.append("M")
    self_dual = True
    for mask in range(1 << n):
        if table[mask] != (1 - table[(~mask) & ((1 << n) - 1)]):
            self_dual = False
            break
    if self_dual:
        classes.append("S")
    anf = _mobius_anf(table, n)
    if _is_linear_anf(anf, n):
        classes.append("L")
    return classes
