from constants import BIT_LENGTH
from converters.decimal_to_binary import trans_into_additional, trans_into_reverse, trans_into_straight


def _unsigned_from_bits(bits: list[int]) -> int:
    value = 0
    for bit in bits:
        value = (value << 1) | bit
    return value


def _bits_to_int_straight(bits: list[int]) -> int:
    sign = -1 if bits[0] == 1 else 1
    magnitude = _unsigned_from_bits(bits[1:])
    return sign * magnitude


def _bits_to_int_reverse(bits: list[int]) -> int:
    sign = -1 if bits[0] == 1 else 1
    magnitude_bits = bits[1:]
    if bits[0] == 1:
        magnitude_bits = [1 - b for b in magnitude_bits]
    magnitude = _unsigned_from_bits(magnitude_bits)
    return sign * magnitude


def _bits_to_int_additional(bits: list[int]) -> int:
    unsigned = _unsigned_from_bits(bits)
    if bits[0] == 0:
        return unsigned
    return unsigned - (1 << BIT_LENGTH)


def test_zero_representation() -> None:
    assert trans_into_straight(0) == [0] * BIT_LENGTH
    assert trans_into_reverse(0) == [0] * BIT_LENGTH
    assert trans_into_additional(0) == [0] * BIT_LENGTH


def test_some_values_roundtrip() -> None:
    values = [0, 1, 2, 5, -1, -2, -5, 123, -123, (1 << 30) - 1, -((1 << 30) - 1)]
    for x in values:
        s = trans_into_straight(x)
        r = trans_into_reverse(x)
        a = trans_into_additional(x)

        assert len(s) == BIT_LENGTH
        assert len(r) == BIT_LENGTH
        assert len(a) == BIT_LENGTH

        assert _bits_to_int_straight(s) == x
        assert _bits_to_int_reverse(r) == x
        assert _bits_to_int_additional(a) == x

