from converters.float32_to_ieee754 import float32_to_ieee754_bits
from operations.operations_with_float import float_add, float_div, float_mul, float_sub


def _float32_expected(x: float) -> float:
    from array import array

    return array("f", [float(x)])[0]


def _float32_bits_expected(x: float) -> list[int]:
    from array import array
    import sys

    packed = array("f", [_float32_expected(x)]).tobytes()
    byteorder = "little" if sys.byteorder == "little" else "big"
    as_int = int.from_bytes(packed, byteorder=byteorder, signed=False)
    bits = [0] * 32
    for i in range(32):
        bits[i] = (as_int >> (31 - i)) & 1
    return bits


def test_float32_add_sub_mul_div() -> None:
    cases = [
        (1.5, 2.25),
        (-1.5, 2.25),
        (3.0, 0.25),
        (10.0, -3.0),
        (-10.0, -3.0),
    ]

    for a, b in cases:
        bits, res = float_add(a, b)
        expected = _float32_expected(a) + _float32_expected(b)
        assert bits == _float32_bits_expected(expected)
        assert res == expected

        bits, res = float_sub(a, b)
        expected = _float32_expected(a) - _float32_expected(b)
        assert bits == _float32_bits_expected(expected)
        assert res == expected

        bits, res = float_mul(a, b)
        expected = _float32_expected(a) * _float32_expected(b)
        assert bits == _float32_bits_expected(expected)
        assert res == expected

        bits, res = float_div(a, b)
        expected = _float32_expected(_float32_expected(a) / _float32_expected(b))
        assert bits == _float32_bits_expected(expected)
        assert res == expected


def test_float32_zero_div_guard() -> None:
    import pytest

    with pytest.raises(ZeroDivisionError):
        float_div(1.0, 0.0)

