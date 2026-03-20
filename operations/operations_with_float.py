from array import array

from converters.float32_to_ieee754 import float32_to_ieee754_bits


def _float32(value: float) -> float:
    return array("f", [float(value)])[0]


def float_add(a: float, b: float) -> tuple[list[int], float]:
    fa = _float32(a)
    fb = _float32(b)
    res = _float32(fa + fb)
    return float32_to_ieee754_bits(res), res


def float_sub(a: float, b: float) -> tuple[list[int], float]:
    fa = _float32(a)
    fb = _float32(b)
    res = _float32(fa - fb)
    return float32_to_ieee754_bits(res), res


def float_mul(a: float, b: float) -> tuple[list[int], float]:
    fa = _float32(a)
    fb = _float32(b)
    res = _float32(fa * fb)
    return float32_to_ieee754_bits(res), res


def float_div(a: float, b: float) -> tuple[list[int], float]:
    fa = _float32(a)
    fb = _float32(b)
    res = _float32(fa / fb)
    return float32_to_ieee754_bits(res), res

