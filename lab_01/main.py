from logic import get_table_with_one_level, get_table_with_more_levels, find_roots


def print_menu():
    print("1 - Вывести таблицу занчений по заданному N и X")
    print("2 - Вывести таблицу занчений по заданному множеству N и единаственному X")
    print("3 - Найти корень уровнения при помощи обратной интерполяции")


def main():
    print_menu()
    choice = int(input("Ваш выбор: "))
    match choice:
        case 1:
            get_table_with_one_level()
        case 2:
            get_table_with_more_levels()
        case 3:
            find_roots()
        case _:
            print("Ошибка!")


if __name__ == "__main__":
    main()