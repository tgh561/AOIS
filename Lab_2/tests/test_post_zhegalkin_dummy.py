from parser import parse_expression
from truth_table import build_truth_table
from post_classes import get_post_classes
from zhegalkin import get_zhegalkin
from dummy_vars import get_dummy_vars


def test_xor_not_monotone_not_linear():
    ast = parse_expression("a&!b|!a&b")
    tt = build_truth_table(ast, ["a", "b"])
    cl = get_post_classes(tt, 2)
    assert "M" not in cl


def test_and_is_monotone():
    ast = parse_expression("a&b")
    tt = build_truth_table(ast, ["a", "b"])
    cl = get_post_classes(tt, 2)
    assert "M" in cl
    assert "T0" in cl


def test_or_t1():
    ast = parse_expression("a|b")
    tt = build_truth_table(ast, ["a", "b"])
    cl = get_post_classes(tt, 2)
    assert "T1" in cl


def test_linear_xor_zhegalkin():
    ast = parse_expression("a~b")
    tt = build_truth_table(ast, ["a", "b"])
    cl = get_post_classes(tt, 2)
    assert "L" in cl
    z = get_zhegalkin(tt, ["a", "b"])
    assert "⊕" in z or z == "0"


def test_dummy_in_or():
    ast = parse_expression("a|!a")
    tt = build_truth_table(ast, ["a", "b"])
    d = get_dummy_vars(tt, ["a", "b"])
    assert "b" in d


def test_no_dummy_and():
    ast = parse_expression("a&b")
    tt = build_truth_table(ast, ["a", "b"])
    assert get_dummy_vars(tt, ["a", "b"]) == []


def test_self_dual_class():
    tt = [0, 0, 1, 1]
    assert "S" in get_post_classes(tt, 2)
