def _lex_to_internal_mask(lex_mask, n):
    internal = 0
    for i in range(n):
        if lex_mask & (1 << (n - 1 - i)):
            internal |= 1 << i
    return internal


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
                    term.append(f"!{vars_list[i]}")
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
                    term.append(f"!{vars_list[i]}")
                else:
                    term.append(vars_list[i])
            terms.append(" | ".join(term))
    return " & ".join(f"({t})" for t in terms) or "1"


def get_numeric_dnf(table):
    n = len(table).bit_length() - 1
    minterms = []
    for lex_mask in range(1 << n):
        if table[_lex_to_internal_mask(lex_mask, n)]:
            minterms.append(lex_mask)
    return f"Σ({', '.join(map(str, minterms))})" if minterms else "Σ(—)"


def get_numeric_cnf(table):
    n = len(table).bit_length() - 1
    maxterms = []
    for lex_mask in range(1 << n):
        if not table[_lex_to_internal_mask(lex_mask, n)]:
            maxterms.append(lex_mask)
    return f"Π({', '.join(map(str, maxterms))})" if maxterms else "Π(—)"


def get_index_form(table):
    n = len(table).bit_length() - 1
    vec = []
    for lex_mask in range(1 << n):
        vec.append(str(table[_lex_to_internal_mask(lex_mask, n)]))
    num = int("".join(vec), 2)
    return f"f = {num}"