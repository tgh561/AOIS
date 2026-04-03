from boolean_function import BooleanFunction


def main():
    print("Анализ булевой функции (переменные a–e, операции &, |, !, ->, ~)")
    expr = input("Формула: ").strip()
    try:
        BooleanFunction(expr).print_all()
    except ValueError as e:
        print(str(e))


if __name__ == "__main__":
    main()
