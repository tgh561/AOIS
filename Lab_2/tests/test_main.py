import builtins
from io import StringIO
import main as main_mod


def test_main_valueerror(monkeypatch, capsys):
    monkeypatch.setattr(builtins, "input", lambda _: "a+")
    main_mod.main()
    out = capsys.readouterr().out
    assert "Недопустимый" in out or "неверный" in out
