from parser import parse_expression
from truth_table import build_truth_table
from boolean_diff import print_derivatives, _derivative


def test_derivative_order1(capsys):
    ast = parse_expression("a&b")
    tt = build_truth_table(ast, ["a", "b"])
    print_derivatives(tt, ["a", "b"])
    out = capsys.readouterr().out
    assert "∂f" in out


def test_partial_derivative_xor():
    ast = parse_expression("(a&!b)|(!a&b)")
    tt = build_truth_table(ast, ["a", "b"])
    d = _derivative(tt, [0])
    assert sum(d) > 0
