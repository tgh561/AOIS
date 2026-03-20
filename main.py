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
    print("Лабораторная: двоичное счисление")
    print("1) Перевести целое в прямой/обратный/дополнительный код")
    print("2) Сложение в дополнительном коде (a + b)")
    print("3) Вычитание в дополнительном коде (a - b)")
    print("4) Умножение в прямом коде (a * b)")
    print("5) Деление в прямом коде с точностью до 5 знаков (a / b)")
    print("6) Операции float32 по IEEE-754-2008 (32 бит)")
    print("7) Сложение в Gray BCD (a + b)")
    print("0) Выход")


def main() -> None:
    while True:
        _menu()
        choice = input("Выберите пункт: ").strip()

        try:
            if choice == "0":
                break

            if choice == "1":
                x = _read_int("Введите целое число x: ")
                s_bits = trans_into_straight(x)
                r_bits = trans_into_reverse(x)
                a_bits = trans_into_additional(x)

                print("Прямой код (2):", _format_bits(s_bits))
                print("Обратный код (2):", _format_bits(r_bits))
                print("Дополнительный код (2):", _format_bits(a_bits))
                print("Десятичное (10):", x)
                print("Проверка декодированием:")
                print("  straight ->", bits_to_decimal_straight(s_bits))
                print("  reverse  ->", bits_to_decimal_reverse(r_bits))
                print("  add      ->", bits_to_decimal_additional(a_bits))

            elif choice == "2":
                a = _read_int("Введите a: ")
                b = _read_int("Введите b: ")
                res_bits = addition(a, b)
                res_dec = bits_to_decimal_additional(res_bits)
                print("Результат (доп. код, 2):", _format_bits(res_bits))
                print("Результат (10):", res_dec)

            elif choice == "3":
                a = _read_int("Введите a: ")
                b = _read_int("Введите b: ")
                res_bits = substraction(a, b)
                res_dec = bits_to_decimal_additional(res_bits)
                print("Результат (доп. код, 2):", _format_bits(res_bits))
                print("Результат (10):", res_dec)

            elif choice == "4":
                a = _read_int("Введите a: ")
                b = _read_int("Введите b: ")
                res_bits = multiplication(a, b)
                res_dec = bits_to_decimal_straight(res_bits)
                print("Результат (прямой код, 2):", _format_bits(res_bits))
                print("Результат (10):", res_dec)

            elif choice == "5":
                a = _read_int("Введите a: ")
                b = _read_int("Введите b: ")
                res_bits = division_direct_fixed(a, b)
                res_dec = bits_to_decimal_direct_fixed(res_bits, DIV_FRAC_BITS)
                print("Результат (прямой код фикс. т., 2):", _format_direct_fixed(res_bits, DIV_FRAC_BITS))
                print("Результат (просто биты):", _format_bits(res_bits))
                print(f"Результат (10) с точностью до {DIV_FRAC_BITS} дробных бит: {res_dec:.5f}")

            elif choice == "6":
                sub = input("Выберите: 1)+ 2)- 3)* 4)/ : ").strip()
                a = _read_float("Введите первое число: ")
                b = _read_float("Введите второе число: ")

                if sub == "1":
                    bits, res_dec = float_add(a, b)
                    op = "+"
                elif sub == "2":
                    bits, res_dec = float_sub(a, b)
                    op = "-"
                elif sub == "3":
                    bits, res_dec = float_mul(a, b)
                    op = "*"
                elif sub == "4":
                    bits, res_dec = float_div(a, b)
                    op = "/"
                else:
                    print("Неизвестная операция.")
                    continue

                print(f"IEEE-754 float32: {a} {op} {b} = {res_dec}")
                print("Биты (2):", _format_bits(bits))
                print("Разбор:", _format_ieee(bits))

            elif choice == "7":
                a = _read_int("Введите a (0..10^8-1): ")
                b = _read_int("Введите b (0..10^8-1): ")
                bits, res_dec = gray_bcd_add(a, b)
                print("Gray BCD (2):", _format_bits(bits))
                print("Сумма (10):", res_dec)

            else:
                print("Неизвестный пункт меню.")

        except ValueError as e:
            print("Ошибка:", e)


if __name__ == "__main__":
    main()