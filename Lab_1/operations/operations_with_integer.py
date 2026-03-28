from constants import BIT_LENGTH, DIV_FRAC_BITS
from converters.decimal_to_binary import trans_into_additional, trans_into_straight


def addition(a: int, b: int) -> list[int]:
    bits_a = trans_into_additional(a)
    bits_b = trans_into_additional(b)
    return _add_additional_bits(bits_a, bits_b)


def _add_additional_bits(bits_a: list[int], bits_b: list[int]) -> list[int]:
    bits_result = [0] * BIT_LENGTH
    carry = 0
    for i in range(BIT_LENGTH - 1, -1, -1):
        temp = bits_a[i] + bits_b[i] + carry
        bits_result[i] = temp % 2
        carry = temp // 2
    return bits_result


def _negate_additional_bits(bits: list[int]) -> list[int]:
    neg_bits = [1 - b for b in bits]
    carry = 1
    for i in range(BIT_LENGTH - 1, -1, -1):
        temp = neg_bits[i] + carry
        neg_bits[i] = temp % 2
        carry = temp // 2
    return neg_bits


def substraction(a: int, b: int) -> list[int]:
    bits_a = trans_into_additional(a)
    bits_b = trans_into_additional(b)
    neg_bits_b = _negate_additional_bits(bits_b)
    return _add_additional_bits(bits_a, neg_bits_b)


def division_direct_fixed(a: int, b: int, frac_bits: int = DIV_FRAC_BITS) -> list[int]:
    if b == 0:
        raise ValueError("Division by zero")

    sign = (a < 0) ^ (b < 0)
    abs_a = abs(a)
    abs_b = abs(b)

    int_bits = BIT_LENGTH - 1 - frac_bits

    integer_part = abs_a // abs_b
    remainder = abs_a % abs_b

    fraction_bits = [0] * frac_bits
    for i in range(frac_bits):
        remainder *= 2
        fraction_bits[i] = remainder // abs_b
        remainder %= abs_b

    integer_mod = integer_part % (1 << int_bits)
    integer_bits = [0] * int_bits
    for i in range(int_bits - 1, -1, -1):
        integer_bits[i] = integer_mod % 2
        integer_mod //= 2

    bits = [0] * BIT_LENGTH
    bits[0] = 1 if sign else 0
    bits[1:] = integer_bits + fraction_bits
    return bits




def multiplication(a: int, b: int) -> list[int]:
    bits_a = trans_into_straight(a)
    bits_b = trans_into_straight(b)
    
    sign = bits_a[0] ^ bits_b[0]
    if a == 0 or b == 0:
        return trans_into_straight(0)
    
    abs_a = abs(a)
    abs_b = abs(b)
    result_int = 0
    
    for _ in range(abs_b):                  
        result_bits = addition(result_int, abs_a)   
        magnitude = 0
        for bit in result_bits[1:]:         
            magnitude = (magnitude << 1) | bit
        result_int = magnitude
        
    final_value = -result_int if sign == 1 else result_int

    return trans_into_straight(final_value)