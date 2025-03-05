from logic import get_table_with_one_level, get_table_with_more_levels, find_roots, find_equation


def print_menu():
    print("1 - Вывести значения по заданному N и X")
    print("2 - Вывести таблицу значений по заданному множеству N и единственному X")
    print("3 - Найти корень уравнения при помощи обратной интерполяции")
    print("4 - Решение системы уравнений")


def main():
    print_menu()
    choice = input("Ваш выбор: ")
    while choice != "0":
        match choice:
            case "1":
                get_table_with_one_level()
            case "2":
                get_table_with_more_levels()
            case "3":
                find_roots()
            case "4":
                find_equation()
            case _:
                print("Введите заново!")
        print_menu()
        choice = input("Ваш выбор: ")
    print("Программа завершена!")


if __name__ == "__main__":
    main()