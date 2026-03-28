from constants import BIT_LENGTH


def _bits_to_unsigned(bits: list[int]) -> int:
    value = 0
    for bit in bits:
        value = (value << 1) | bit
    return value


def bits_to_decimal_straight(bits: list[int]) -> int:
    sign = -1 if bits[0] == 1 else 1
    magnitude = _bits_to_unsigned(bits[1:])
    return sign * magnitude


def bits_to_decimal_reverse(bits: list[int]) -> int:
    sign = -1 if bits[0] == 1 else 1
    magnitude_bits = bits[1:]
    if bits[0] == 1:
        magnitude_bits = [1 - b for b in magnitude_bits]
    magnitude = _bits_to_unsigned(magnitude_bits)
    return sign * magnitude


def bits_to_decimal_additional(bits: list[int]) -> int:
    unsigned = _bits_to_unsigned(bits)
    if bits[0] == 0:
        return unsigned
    return unsigned - (1 << BIT_LENGTH)


def bits_to_decimal_direct_fixed(bits: list[int], frac_bits: int) -> float:
    """
    Direct code (sign-magnitude) with a binary point.
    bits layout: [sign][integer bits][fraction bits]
    """
    sign = -1.0 if bits[0] == 1 else 1.0
    int_bits = BIT_LENGTH - 1 - frac_bits
    integer_part = _bits_to_unsigned(bits[1 : 1 + int_bits])
    fraction_part_bits = bits[1 + int_bits :]
    fraction_value = 0.0
    for i, bit in enumerate(fraction_part_bits):
        fraction_value += bit / (2 ** (i + 1))
    return sign * (integer_part + fraction_value)
