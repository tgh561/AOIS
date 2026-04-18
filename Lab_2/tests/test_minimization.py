from parser import parse_expression
from truth_table import build_truth_table
from minimization.quine_mccluskey import quine_mccluskey_minimize
from minimization.karnaugh import print_karnaugh_map, karnaugh_minimize


def test_qm_constant_zero(capsys):
    ast = parse_expression("a&!a")
    tt = build_truth_table(ast, ["a"])
    quine_mccluskey_minimize(tt, ["a"], show_stages=False, method="calc", form="dnf")
    out = capsys.readouterr().out
    assert "0" in out


def test_qm_constant_one(capsys):
    ast = parse_expression("a|!a")
    tt = build_truth_table(ast, ["a"])
    quine_mccluskey_minimize(tt, ["a"], show_stages=False, method="calc", form="dnf")
    out = capsys.readouterr().out
    assert "1" in out


def test_qm_xor_like(capsys):
    ast = parse_expression("a&!b|!a&b")
    tt = build_truth_table(ast, ["a", "b"])
    quine_mccluskey_minimize(tt, ["a", "b"], show_stages=True, method="table", form="dnf")
    out = capsys.readouterr().out
    assert "Минимальная ДНФ" in out
    assert "Таблица покрытия" in out


def test_qm_cnf_or(capsys):
    ast = parse_expression("a|b")
    tt = build_truth_table(ast, ["a", "b"])
    quine_mccluskey_minimize(tt, ["a", "b"], show_stages=False, method="calc", form="cnf")
    out = capsys.readouterr().out
    assert "Минимальная КНФ" in out
    assert "|" in out


def test_karnaugh_three_vars(capsys):
    ast = parse_expression("a|b&c")
    tt = build_truth_table(ast, ["a", "b", "c"])
    print_karnaugh_map(tt, ["a", "b", "c"])
    out = capsys.readouterr().out
    assert "\\" in out or "bc" in out


def test_karnaugh_four_vars(capsys):
    ast = parse_expression("a&b|c&d")
    tt = build_truth_table(ast, list("abcd"))
    print_karnaugh_map(tt, list("abcd"))
    out = capsys.readouterr().out
    assert "ab" in out or "cd" in out


def test_karnaugh_five_vars_two_planes(capsys):
    ast = parse_expression("(a&!b&!c&d)|!e")
    tt = build_truth_table(ast, list("abcde"))
    print_karnaugh_map(tt, list("abcde"))
    out = capsys.readouterr().out
    assert "e = 0" in out and "e = 1" in out
    assert "ab \\ cd" in out


def test_karnaugh_minimize_dnf(capsys):
    ast = parse_expression("(a&b)|(!a&b)")
    tt = build_truth_table(ast, ["a", "b"])
    karnaugh_minimize(tt, ["a", "b"], form="dnf", show_groups=True)
    out = capsys.readouterr().out
    assert "Минимальная ДНФ" in out


def test_karnaugh_minimize_cnf(capsys):
    ast = parse_expression("a|b")
    tt = build_truth_table(ast, ["a", "b"])
    karnaugh_minimize(tt, ["a", "b"], form="cnf", show_groups=True)
    out = capsys.readouterr().out
    assert "Минимальная КНФ" in out


def test_karnaugh_zero_vars(capsys):
    print_karnaugh_map([1], [])
    out = capsys.readouterr().out
    assert "f =" in out


def test_karnaugh_one_var(capsys):
    print_karnaugh_map([0, 1], ["a"])
    out = capsys.readouterr().out
    assert "a" in out


def test_qm_merge_two_fail_branch():
    from minimization import quine_mccluskey as qm
    assert qm._merge_two((0, 7), (7, 7)) is None
