from constants import BIT_LENGTH, DIV_FRAC_BITS, BCD_DIGITS


def test_constants_values() -> None:
    assert BIT_LENGTH == 32
    assert DIV_FRAC_BITS == 5
    assert BCD_DIGITS == 8

