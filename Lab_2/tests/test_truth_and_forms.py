import pytest
from parser import parse_expression
from truth_table import build_truth_table, _evaluate_ast
from normal_forms import get_dnf, get_cnf, get_numeric_dnf, get_numeric_cnf, get_index_form


def test_equivalence_truth():
    ast = parse_expression("a~b")
    tt = build_truth_table(ast, ["a", "b"])
    assert tt == [1, 0, 0, 1]


def test_implication():
    ast = parse_expression("a->b")
    tt = build_truth_table(ast, ["a", "b"])
    assert tt == [1, 0, 1, 1]


def test_index_form():
    ast = parse_expression("a&b")
    tt = build_truth_table(ast, ["a", "b"])
    idx = get_index_form(tt)
    assert "f = " in idx


def test_numeric_forms_nand():
    ast = parse_expression("!(a&b)")
    tt = build_truth_table(ast, ["a", "b"])
    assert "Σ" in get_numeric_dnf(tt)
    assert "Π" in get_numeric_cnf(tt)


def test_dnf_cnf_constants():
    table0 = [0, 0, 0, 0]
    assert get_dnf(table0, ["a", "b"]) == "0"
    assert get_cnf(table0, ["a", "b"]) != "1"
    table1 = [1, 1, 1, 1]
    assert get_cnf(table1, ["a", "b"]) == "1"


def test_evaluate_ast_unknown_var():
    ast = "a"
    assert _evaluate_ast(ast, {"a": True}) is True
    assert _evaluate_ast(ast, {}) is False


def test_evaluate_ast_bad_node():
    assert _evaluate_ast(["a", "%", "b"], {"a": True, "b": True}) is False
