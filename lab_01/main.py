from logic import get_table


def print_menu():
    print("1 - Вывести таблицу занчений")


def main():
    print_menu()
    choice = int(input("Ваш выбор: "))
    match choice != 0:
        case 1:
            get_table()
        case _:
            print("Ошибка!")

if __name__ == "__main__":
    main()