from boolean_function import BooleanFunction


def main():
    print("Операции из задания: &, |, ! (отрицание), -> (импликация), ~ (эквиваленция)")
    expr = input("Формула: ").strip()
    try:
        BooleanFunction(expr).print_all()
    except ValueError as e:
        print(str(e))


if __name__ == "__main__":
    main()
