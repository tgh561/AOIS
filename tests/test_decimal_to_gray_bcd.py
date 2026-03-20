import pytest

from constants import BCD_DIGITS
from converters.decimal_to_gray_bcd import decimal_to_gray_bcd_bits


def _digit_to_gray_bcd_bits(digit: int) -> list[int]:
    gray = digit ^ (digit >> 1)
    return [(gray >> k) & 1 for k in range(3, -1, -1)]


def _expected_gray_bcd_bits(value: int, digits: int) -> list[int]:
    dec_digits = [0] * digits
    x = value
    for i in range(digits - 1, -1, -1):
        dec_digits[i] = x % 10
        x //= 10
    bits: list[int] = []
    for d in dec_digits:
        bits.extend(_digit_to_gray_bcd_bits(d))
    return bits


def test_gray_bcd_simple_values() -> None:
    assert decimal_to_gray_bcd_bits(0, digits=4) == _expected_gray_bcd_bits(0, digits=4)
    assert decimal_to_gray_bcd_bits(1, digits=4) == _expected_gray_bcd_bits(1, digits=4)
    assert decimal_to_gray_bcd_bits(9, digits=4) == _expected_gray_bcd_bits(9, digits=4)
    assert decimal_to_gray_bcd_bits(10, digits=4) == _expected_gray_bcd_bits(10, digits=4)
    assert decimal_to_gray_bcd_bits(12, digits=4) == _expected_gray_bcd_bits(12, digits=4)


def test_gray_bcd_digits_length() -> None:
    bits = decimal_to_gray_bcd_bits(12345678, digits=BCD_DIGITS)
    assert len(bits) == BCD_DIGITS * 4


def test_gray_bcd_rejects_negative() -> None:
    with pytest.raises(ValueError):
        decimal_to_gray_bcd_bits(-1, digits=4)


def test_gray_bcd_rejects_overflow() -> None:
    with pytest.raises(ValueError):
        decimal_to_gray_bcd_bits(10000, digits=4)

