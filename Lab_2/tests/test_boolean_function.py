import pytest
from boolean_function import BooleanFunction


def test_constructor_and_vars():
    f = BooleanFunction("  a & b  ")
    assert f.vars == ["a", "b"]
    assert len(f.truth_table) == 4


def test_print_all_runs(capsys):
    BooleanFunction("a->b").print_all()
    out = capsys.readouterr().out
    assert "СДНФ" in out
    assert "СКНФ" in out
    assert "карта карно" in out.lower()
    assert "Минимальная КНФ" in out
    assert "Классы Поста" in out


def test_invalid_raises():
    with pytest.raises(ValueError):
        BooleanFunction("a+")


def test_double_negation_vars(capsys):
    BooleanFunction("!!a").print_all()
    assert "a" in capsys.readouterr().out
