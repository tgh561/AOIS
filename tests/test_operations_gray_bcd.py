import pytest

from constants import BCD_DIGITS
from converters.decimal_to_gray_bcd import decimal_to_gray_bcd_bits
from operations.operations_with_gray_bcd import gray_bcd_add


def test_gray_bcd_add_basic() -> None:
    cases = [
        (0, 0),
        (12, 34),
        (95, 10),
        (1234, 5678),
        (99999999 - 1, 1),
    ]
    for a, b in cases:
        bits, dec_sum = gray_bcd_add(a, b, digits=BCD_DIGITS)
        assert dec_sum == a + b
        assert len(bits) == BCD_DIGITS * 4

        expected_bits = decimal_to_gray_bcd_bits(dec_sum, digits=BCD_DIGITS)
        assert bits == expected_bits


def test_gray_bcd_add_rejects_negative() -> None:
    with pytest.raises(ValueError):
        gray_bcd_add(-1, 1)


def test_gray_bcd_add_overflow_raises() -> None:
    with pytest.raises(ValueError):
        gray_bcd_add(99, 1, digits=2)

