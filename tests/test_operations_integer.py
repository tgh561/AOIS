import pytest

from constants import BIT_LENGTH, DIV_FRAC_BITS
from converters.decimal_to_binary import trans_into_straight
from converters.binary_to_decimal import bits_to_decimal_additional, bits_to_decimal_direct_fixed, bits_to_decimal_straight
from operations.operations_with_integer import addition, division_direct_fixed, multiplication, substraction


def _fixed_div_trunc(a: int, b: int, frac_bits: int) -> float:
    if b == 0:
        raise ValueError("Division by zero")
    sign = -1 if (a < 0) ^ (b < 0) else 1
    abs_a = abs(a)
    abs_b = abs(b)
    scale = 1 << frac_bits
    magnitude = (abs_a * scale) // abs_b / scale
    return sign * magnitude


def test_addition_in_additional_code() -> None:
    cases = [
        (3, 5),
        (-3, 5),
        (3, -5),
        (-3, -5),
        (1234, -12),
        (100, 200),
        (-100, 200),
        (-100, -200),
    ]
    for a, b in cases:
        res_bits = addition(a, b)
        assert bits_to_decimal_additional(res_bits) == a + b


def test_subtraction_in_additional_code() -> None:
    cases = [
        (3, 5),
        (-3, 5),
        (3, -5),
        (-3, -5),
        (1234, -12),
        (100, -100),
        (-100, 200),
    ]
    for a, b in cases:
        res_bits = substraction(a, b)
        assert bits_to_decimal_additional(res_bits) == a - b


def test_multiplication_in_direct_code() -> None:
    cases = [
        (3, 5),
        (-3, 5),
        (3, -5),
        (-3, -5),
        (12, 13),
        (-12, -13),
        (1000, 20),
        (-1000, -20),
    ]
    for a, b in cases:
        res_bits = multiplication(a, b)
        assert bits_to_decimal_straight(res_bits) == a * b


@pytest.mark.parametrize("a,b", [(7, 3), (1, 2), (5, 2), (-7, 3), (7, -3), (-7, -3), (123, 7)])
def test_division_direct_fixed_precision_5_bits(a: int, b: int) -> None:
    bits = division_direct_fixed(a, b, frac_bits=DIV_FRAC_BITS)
    got = bits_to_decimal_direct_fixed(bits, frac_bits=DIV_FRAC_BITS)
    expected = _fixed_div_trunc(a, b, DIV_FRAC_BITS)
    assert got == pytest.approx(expected, abs=1e-9)


def test_division_direct_by_zero() -> None:
    with pytest.raises(ValueError):
        division_direct_fixed(1, 0)

