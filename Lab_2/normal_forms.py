def get_dnf(table, vars_list):
    n = len(vars_list)
    terms = []
    for mask in range(1 << n):
        if table[mask]:
            term = []
            for i in range(n):
                if mask & (1 << i):
                    term.append(vars_list[i])
                else:
                    term.append(f"~{vars_list[i]}")
            terms.append(" & ".join(term))
    return " | ".join(terms) or "0"


def get_cnf(table, vars_list):
    n = len(vars_list)
    terms = []
    for mask in range(1 << n):
        if not table[mask]:
            term = []
            for i in range(n):
                if mask & (1 << i):
                    term.append(f"~{vars_list[i]}")
                else:
                    term.append(vars_list[i])
            terms.append(" | ".join(term))
    return " & ".join(f"({t})" for t in terms) or "1"


def get_numeric_dnf(table):
    minterms = [i for i, v in enumerate(table) if v]
    return f"Σ({', '.join(map(str, minterms))})" if minterms else "Σ(—)"


def get_numeric_cnf(table):
    maxterms = [i for i, v in enumerate(table) if not v]
    return f"Π({', '.join(map(str, maxterms))})" if maxterms else "Π(—)"


def get_index_form(table):
    num = int("".join(map(str, table[::-1])), 2)   # младший бит = a
    return f"f = {num}"