def build_truth_table(ast, vars_list):
    n = len(vars_list)
    table = [0] * (1 << n)
    for mask in range(1 << n):
        assignment = {vars_list[i]: bool(mask & (1 << i)) for i in range(n)}
        table[mask] = 1 if _evaluate_ast(ast, assignment) else 0
    return table


def _evaluate_ast(node, assignment):
    if isinstance(node, str):
        return assignment.get(node, False)
    if isinstance(node, list):
        if node[0] == "!":
            return not _evaluate_ast(node[1], assignment)
        left = _evaluate_ast(node[0], assignment)
        right = _evaluate_ast(node[2], assignment)
        op = node[1]
        if op == "&":
            return left and right
        if op == "|":
            return left or right
        if op == "->":
            return (not left) or right
        if op == "~":
            return left == right
    return False


def print_truth_table(table, vars_list):
    n = len(vars_list)
    print("Таблица истинности:")
    header = " ".join(vars_list) + " | f"
    print(header)
    print("-" * len(header))
    for mask in range(1 << n):
        row = " ".join("1" if (mask & (1 << i)) else "0" for i in range(n))
        print(row, "|", table[mask])
