from converters.float32_to_ieee754 import float32_to_ieee754_bits


def _expected_bits(x: float) -> list[int]:
    from array import array
    import sys

    packed = array("f", [float(x)]).tobytes()
    byteorder = "little" if sys.byteorder == "little" else "big"
    as_int = int.from_bytes(packed, byteorder=byteorder, signed=False)
    bits = [0] * 32
    for i in range(32):
        bits[i] = (as_int >> (31 - i)) & 1
    return bits


def test_ieee_bits_basic_values() -> None:
    for x in [0.0, 1.0, -1.0, 1.5, -2.25, 10.0, -3.0, 123.75]:
        assert float32_to_ieee754_bits(x) == _expected_bits(x)

