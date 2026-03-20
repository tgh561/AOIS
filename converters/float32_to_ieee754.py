import sys
from array import array


def float32_to_ieee754_bits(value: float) -> list[int]:
    packed = array("f", [float(value)]).tobytes()
    byteorder = "little" if sys.byteorder == "little" else "big"
    as_int = int.from_bytes(packed, byteorder=byteorder, signed=False)
    bits = [0] * 32
    for i in range(32):
        bits[i] = (as_int >> (31 - i)) & 1
    return bits

