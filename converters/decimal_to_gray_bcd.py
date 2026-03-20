from constants import BCD_DIGITS


def _decimal_digit_to_gray_bcd(digit: int) -> list[int]:
    gray = digit ^ (digit >> 1)
    return [(gray >> k) & 1 for k in range(3, -1, -1)]


def decimal_to_gray_bcd_bits(value: int, digits: int = BCD_DIGITS) -> list[int]:
    if value < 0:
        raise ValueError("Gray BCD: value must be non-negative")
    max_value = 10**digits
    if value >= max_value:
        raise ValueError("Gray BCD: value is too large for selected digits")

    dec_digits = [0] * digits
    x = value
    for i in range(digits - 1, -1, -1):
        dec_digits[i] = x % 10
        x //= 10

    bits: list[int] = []
    for digit in dec_digits:
        bits.extend(_decimal_digit_to_gray_bcd(digit))
    return bits

