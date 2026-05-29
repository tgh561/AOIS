from src.hash_table import HashTable

TABLE_SIZE = 23

data = {
    "Существительное": "Часть речи, обозначающая предмет",
    "Глагол": "Часть речи, обозначающая действие",
    "Прилагательное": "Часть речи, обозначающая признак",
    "Местоимение": "Указывает на предмет, но не называет его",
    "Наречие": "Обозначает признак действия",
    "Подлежащее": "Главный член предложения",
    "Сказуемое": "Главный член предложения, обозначающий действие",
    "Суффикс": "Значимая часть слова",
    "Приставка": "Часть слова перед корнем",
    "Корень": "Главная значимая часть слова",
    "Окончание": "Изменяемая часть слова",
    "Фонетика": "Раздел грамматики о звуках",
    "Синтаксис": "Раздел грамматики о предложениях",
    "Морфология": "Раздел грамматики о частях речи",
    "Пунктуация": "Правила постановки знаков препинания",
}


def print_chain(row):
    current = row

    while current:
        print(
            f"[{current.id}: {current.pi}]",
            end=""
        )

        if current.next:
            print(" -> ", end="")

        current = current.next

    print()


def main():
    table = HashTable(TABLE_SIZE)

    for key, value in data.items():
        table.insert(key, value)

    while True:
        print(
            "\nМеню\n\n"
            "1. Показать таблицу\n"
            "2. Добавить пару\n"
            "3. Найти по значению\n"
            "4. Удалить по значению\n"
            "0. Выход\n"
        )

        try:
            choise = int(input("Выбор:"))

        except:
            print("Неверный формат ввода")
            continue

        try:
            match choise:

                case 0:
                    break

                case 1:
                    print(
                        f"{'№':<3} | "
                        f"{'V':<5} | "
                        f"{'h(v)':<5} | "
                        f"{'ID':<20} | "
                        f"C U T L D | "
                        f"P0 | "
                        f"P1"
                    )

                    print("-" * 120)

                    for index, row in enumerate(table.rows):

                        if row.u == 0:
                            print(
                                f"{index:<3} | "
                                f"{0:<5} | "
                                f"{0:<5} | "
                                f"{'-':<20} | "
                                f"0 0 1 0 0 | "
                                f"{row.p0:<2} | "
                                f"-"
                            )

                            continue

                        current = row

                        while current:

                            v = table._calc_hash(current.id)
                            h = table._define_index(v)

                            flags = (
                                f"{current.c} "
                                f"{current.u} "
                                f"{current.t} "
                                f"{current.l} "
                                f"{current.d}"
                            )

                            print(
                                f"{index:<3} | "
                                f"{v:<5} | "
                                f"{h:<5} | "
                                f"{current.id[:19]:<20} | "
                                f"{flags} | "
                                f"{current.p0:<2} | "
                                f"{current.pi[:40]}"
                            )

                            current = current.next

                    print(
                        f"\nКоэффицент заполнения: "
                        f"{table.get_fill_factor():.2f}"
                    )

                case 2:
                    key = input("Введите ключ:")
                    value = input("Введите значение:")

                    result = table.insert(key, value)

                    if result:
                        print(f"Пара {key}: {value} добавлена")

                    else:
                        print("Пара уже есть в таблице")

                case 3:
                    key = input("Введите ключ:")

                    result = table.search(key)

                    if result:
                        _, _, value = result

                        print(f"Найденное значение: {value}")

                    else:
                        print("Такого значения не найдено")

                case 4:
                    key = input("Введите ключ:")

                    result = table.delete(key)

                    if result:
                        _, _, value = result

                        print(
                            f"Удалена пара значений "
                            f"{key}: {value}"
                        )

                    else:
                        print("Такого значения не найдено")

                case _:
                    print("Выбрана невозможная операция")
                    break

        except:
            print("Ошибка выполнения, попробуйте еще раз")
            continue


if __name__ == "__main__":
    main()