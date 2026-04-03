_ARROW = "\x00"

def normalize_expression(s: str) -> str:
    s = s.strip().replace(" ", "")
    repl = (
        ("∨", "|"),
        ("\u2228", "|"),
        ("∧", "&"),
        ("\u2227", "&"),
        ("¬", "!"),
        ("\u00ac", "!"),
        ("→", _ARROW),
        ("\u2192", _ARROW),
        ("↔", "~"),
        ("\u2194", "~"),
    )
    for a, b in repl:
        s = s.replace(a, b)
    s = s.replace("->", _ARROW)
    return s


def _validate_chars(s: str) -> None:
    t = s.replace(_ARROW, "")
    for ch in t:
        if ch not in "abcde()!&|~":
            raise ValueError(f"Недопустимый символ в выражении: {repr(ch)}")


def _balanced_parens(s: str) -> bool:
    depth = 0
    for ch in s:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth < 0:
                return False
    return depth == 0


def parse_one_brackets(string: str):
    if not (string and string[0] == "(" and string[-1] == ")"):
        return None
    inner = string[1:-1].strip()
    if not _balanced_parens(inner):
        return None
    return parsing(inner)


def find_main_operator(s: str):
    if not s:
        return None, None
    operators = {
        "~": (0, "left"),
        "->": (1, "right"),
        "|": (2, "left"),
        "&": (3, "left"),
    }
    min_pri = float("inf")
    pos = -1
    op_found = None
    bracket_level = 0
    i = 0
    while i < len(s):
        ch = s[i]
        if ch == "(":
            bracket_level += 1
        elif ch == ")":
            bracket_level -= 1
        elif bracket_level == 0:
            current_op = None
            op_len = 1
            if i + 1 < len(s) and s[i : i + 2] == "->":
                current_op = "->"
                op_len = 2
            elif ch == "|":
                current_op = "|"
            elif ch == "&":
                current_op = "&"
            elif ch == "~":
                current_op = "~"

            if current_op:
                pri, assoc = operators[current_op]
                update = False
                if pri < min_pri:
                    update = True
                elif pri == min_pri and assoc == "left":
                    update = True
                if update:
                    min_pri = pri
                    pos = i
                    op_found = current_op
                i += op_len - 1
        i += 1
    return (pos, op_found) if pos != -1 else (None, None)


def parsing(string: str):
    string = string.strip()
    if not string:
        return None
    if not _balanced_parens(string):
        return None

    parsed = parse_one_brackets(string)
    if parsed is not None:
        return parsed

    op_pos, op = find_main_operator(string)
    if op is not None:
        left = string[:op_pos]
        right = string[op_pos + len(op) :]
        if not left.strip() or not right.strip():
            return None
        return [parsing(left), op, parsing(right)]

    if string.startswith("!"):
        inner = parsing(string[1:])
        if inner is None:
            return None
        return ["!", inner]

    if len(string) == 1 and string in "abcde":
        return string

    return None


def parse_expression(expr: str):
    if not expr or not expr.strip():
        raise ValueError("Пустое выражение.")
    raw = expr.strip()
    normalized = normalize_expression(raw)
    _validate_chars(normalized)
    s = normalized.replace(_ARROW, "->")
    tree = parsing(s)
    if tree is None:
        raise ValueError("Выражение имеет неверный синтаксис (проверьте скобки и операторы).")
    vars_set = set()

    def collect_vars(node):
        if isinstance(node, str):
            if node in "abcde":
                vars_set.add(node)
            elif node not in ("!",):
                pass
        elif isinstance(node, list):
            if node[0] == "!":
                collect_vars(node[1])
            else:
                collect_vars(node[0])
                collect_vars(node[2])

    collect_vars(tree)
    return tree
