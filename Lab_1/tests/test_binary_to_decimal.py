from constants import BIT_LENGTH, DIV_FRAC_BITS
from converters.decimal_to_binary import trans_into_additional, trans_into_reverse, trans_into_straight
from converters.binary_to_decimal import (
    bits_to_decimal_additional,
    bits_to_decimal_direct_fixed,
    bits_to_decimal_reverse,
    bits_to_decimal_straight,
)


def test_decode_straight_reverse_additional() -> None:
    values = [0, 1, 2, 5, -1, -2, -5, 123, -123, (1 << 30) - 1, -((1 << 30) - 1)]
    for x in values:
        s_bits = trans_into_straight(x)
        r_bits = trans_into_reverse(x)
        a_bits = trans_into_additional(x)

        assert bits_to_decimal_straight(s_bits) == x
        assert bits_to_decimal_reverse(r_bits) == x
        assert bits_to_decimal_additional(a_bits) == x


def test_decode_direct_fixed_division_format() -> None:
    from operations.operations_with_integer import division_direct_fixed

    cases = [(7, 3), (-7, 3), (7, -3), (-7, -3), (1, 2)]
    for a, b in cases:
        bits = division_direct_fixed(a, b, frac_bits=DIV_FRAC_BITS)
        value = bits_to_decimal_direct_fixed(bits, frac_bits=DIV_FRAC_BITS)
        assert isinstance(value, float)

