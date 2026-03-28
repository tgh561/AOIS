import builtins

import main as lab_main


def test_main_menu_integer_and_gray_bcd_branches(monkeypatch) -> None:
    inputs = iter(
        [
            "1",
            "-5",
            "2",
            "3",
            "5",
            "3",
            "3",
            "5",
            "4",
            "3",
            "5",
            "5",
            "7",
            "3",
            "7",
            "12",
            "34",
            "0",
        ]
    )

    def fake_input(prompt: str = "") -> str:
        return next(inputs)

    monkeypatch.setattr(builtins, "input", fake_input)

    lab_main.main()

