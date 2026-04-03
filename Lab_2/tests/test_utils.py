from utils import print_header


def test_print_header(capsys):
    print_header("test")
    out = capsys.readouterr().out
    assert "test" in out
    assert "=" in out
