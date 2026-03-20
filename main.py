from constants import BIT_LENGTH, DIV_FRAC_BITS
from converters.decimal_to_binary import trans_into_straight, trans_into_reverse, trans_into_additional
from converters.binary_to_decimal import (
    bits_to_decimal_straight,
    bits_to_decimal_reverse,
    bits_to_decimal_additional,
    bits_to_decimal_direct_fixed,
)
from operations.operations_with_integer import addition, multiplication, substraction, division_direct_fixed
from operations.operations_with_float import float_add, float_sub, float_mul, float_div
from operations.operations_with_gray_bcd import gray_bcd_add


def _read_int(prompt: str) -> int:
    return int(input(prompt).strip())


def _read_float(prompt: str) -> float:
    s = input(prompt).strip().replace(",", ".")
    return float(s)


def _format_bits(bits: list[int], group: int = 4) -> str:
    parts = []
    for i in range(0, len(bits), group):
        parts.append("".join(str(b) for b in bits[i : i + group]))
    return " ".join(parts)


def _format_direct_fixed(bits: list[int], frac_bits: int) -> str:
    int_bits = BIT_LENGTH - 1 - frac_bits
    sign = bits[0]
    integer_part = bits[1 : 1 + int_bits]
    fraction_part = bits[1 + int_bits :]
    return f"S={sign} | {''.join(map(str, integer_part))}.{''.join(map(str, fraction_part))}"


def _format_ieee(bits: list[int]) -> str:
    sign = bits[0]
    exponent = bits[1:9]
    mantissa = bits[9:]
    return f"sign={sign}, exp={''.join(map(str, exponent))}, mant={''.join(map(str, mantissa))}"


def _menu() -> None:
    print("1) коды x")
    print("2) a+b (доп.)")
    print("3) a-b (доп.)")
    print("4) a*b (прям.)")
    print("5) a/b (прям.,5 дроб.)")
    print("6) float32 (+-*/)")
    print("7) a+b (Gray BCD)")
    print("0) exit")


def main() -> None:
    while True:
        _menu()
        choice = input("> ").strip()

        try:
            if choice == "0":
                break

            if choice == "1":
                x = _read_int("x: ")
                s_bits = trans_into_straight(x)
                r_bits = trans_into_reverse(x)
                a_bits = trans_into_additional(x)

                print("s:", _format_bits(s_bits))
                print("r:", _format_bits(r_bits))
                print("a:", _format_bits(a_bits))
                print("10:", x)
                print(
                    "dec:",
                    bits_to_decimal_straight(s_bits),
                    bits_to_decimal_reverse(r_bits),
                    bits_to_decimal_additional(a_bits),
                )

            elif choice == "2":
                a = _read_int("a: ")
                b = _read_int("b: ")
                res_bits = addition(a, b)
                res_dec = bits_to_decimal_additional(res_bits)
                print("2:", _format_bits(res_bits))
                print("10:", res_dec)

            elif choice == "3":
                a = _read_int("a: ")
                b = _read_int("b: ")
                res_bits = substraction(a, b)
                res_dec = bits_to_decimal_additional(res_bits)
                print("2:", _format_bits(res_bits))
                print("10:", res_dec)

            elif choice == "4":
                a = _read_int("a: ")
                b = _read_int("b: ")
                res_bits = multiplication(a, b)
                res_dec = bits_to_decimal_straight(res_bits)
                print("2:", _format_bits(res_bits))
                print("10:", res_dec)

            elif choice == "5":
                a = _read_int("a: ")
                b = _read_int("b: ")
                res_bits = division_direct_fixed(a, b)
                res_dec = bits_to_decimal_direct_fixed(res_bits, DIV_FRAC_BITS)
                print("2:", _format_direct_fixed(res_bits, DIV_FRAC_BITS))
                print("10:", f"{res_dec:.5f}")

            elif choice == "6":
                op = input("op(+ - * /): ").strip()
                a = _read_float("a: ")
                b = _read_float("b: ")

                if op == "+":
                    bits, res_dec = float_add(a, b)
                    sym = "+"
                elif op == "-":
                    bits, res_dec = float_sub(a, b)
                    sym = "-"
                elif op == "*":
                    bits, res_dec = float_mul(a, b)
                    sym = "*"
                elif op == "/":
                    bits, res_dec = float_div(a, b)
                    sym = "/"
                else:
                    print("bad op")
                    continue

                print("2:", _format_bits(bits))
                print("10:", f"{res_dec}")

            elif choice == "7":
                a = _read_int("a: ")
                b = _read_int("b: ")
                bits, res_dec = gray_bcd_add(a, b)
                print("2:", _format_bits(bits))
                print("10:", res_dec)

            else:
                print("bad choice")

        except ValueError as e:
            print("err:", e)


if __name__ == "__main__":
    main()