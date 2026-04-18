import pytest
from parser import parse_expression, normalize_expression, parsing


def test_normalize_unicode_implication_or():
    s = normalize_expression("!(!a→!b)∨c")
    assert "c" in s
    assert "→" not in s
    assert "∨" not in s


def test_parse_unicode_example():
    tree = parse_expression("!(!a→!b)∨c")
    assert tree is not None


def test_equivalence_ast():
    tree = parse_expression("a~b")
    assert tree[1] == "~"


def test_precedence_implication_over_or():
    tree = parse_expression("a|b->c")
    assert tree[1] == "->"
    left = tree[0]
    assert isinstance(left, list) and left[1] == "|"


def test_empty_raises():
    with pytest.raises(ValueError, match="Пустое"):
        parse_expression("   ")


def test_invalid_symbol_raises():
    with pytest.raises(ValueError, match="Недопустимый"):
        parse_expression("a+x")


def test_invalid_syntax_raises():
    with pytest.raises(ValueError, match="неверный синтаксис"):
        parse_expression("a&")


def test_tilde_is_binary_equivalence_only():
    with pytest.raises(ValueError, match="неверный синтаксис"):
        parse_expression("~a")


def test_negation_is_bang():
    assert parse_expression("!a") == ["!", "a"]


def test_balanced_parens_required():
    with pytest.raises(ValueError, match="неверный синтаксис"):
        parse_expression("(a|b")


def test_double_negation():
    tree = parse_expression("!!a")
    assert tree[0] == "!"


def test_parsing_internal_used():
    assert parsing("(a&b)") is not None


def test_parse_one_brackets_unbalanced_inner():
    assert parsing("(()") is None


