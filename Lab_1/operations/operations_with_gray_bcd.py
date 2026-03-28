from constants import BCD_DIGITS


def _digit_to_gray_bcd_bits(digit: int) -> list[int]:
    gray = digit ^ (digit >> 1)
    return [(gray >> k) & 1 for k in range(3, -1, -1)]


def gray_bcd_add(a: int, b: int, digits: int = BCD_DIGITS) -> tuple[list[int], int]:
    if a < 0 or b < 0:
        raise ValueError("Gray BCD: a and b must be non-negative")

    max_value = 10**digits
    if a >= max_value or b >= max_value:
        raise ValueError("Gray BCD: inputs are too large for selected digits")

    a_digits = [0] * digits
    b_digits = [0] * digits

    x = a
    for i in range(digits - 1, -1, -1):
        a_digits[i] = x % 10
        x //= 10

    x = b
    for i in range(digits - 1, -1, -1):
        b_digits[i] = x % 10
        x //= 10

    carry = 0
    res_digits = [0] * digits
    for i in range(digits - 1, -1, -1):
        s = a_digits[i] + b_digits[i] + carry
        if s >= 10:
            s -= 10
            carry = 1
        else:
            carry = 0
        res_digits[i] = s

    if carry == 1:
        raise ValueError("Gray BCD: overflow beyond selected digits")

    bits: list[int] = []
    for digit in res_digits:
        bits.extend(_digit_to_gray_bcd_bits(digit))

    return bits, a + b

