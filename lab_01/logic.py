from logic_of_newton_polynomial import get_newton_value
from logic_of_hermite_polynomial import get_hermite_value
from utils import read_point_table, read_from_file
from settings import FILE_TABLE_1, FILE_TABLE_2, FILE_TABLE_3


def print_header_of_table(x: float):
    print(f"Данные при x = {x}")
    print("|--------------------------------|")
    print("| Степень  | Полином  | Полином  |")
    print("| полинома | Ньютона  | Эрмита   |")
    print("|--------------------------------|")


def print_row_of_table(polynom: int, result_newton: float, result_hermite: float):
    print("|{:10d}|{:10.5f}|{:10.5f}|".format(polynom, result_newton, result_hermite))
    print("|--------------------------------|")


def diff_data(table, x, y, y_derivative):
    for i in table:
        x.append(i[0])
        y.append(i[1])
        y_derivative.append(i[2])


def get_table_with_one_level():
    # Чтение таблицы из файла
    table = read_point_table(FILE_TABLE_1)  # Используем функцию read_point_table

    # Ввод данных пользователем
    level_of_polynomial = int(input("Введите степень полинома Ньютона/количество узлов полинома Эрмита для нахождения значения: "))
    x_finder = float(input("Введите X для подсчета значения: "))

    # Вычисление значения полинома Ньютона
    result_newton = get_newton_value(table, level_of_polynomial, x_finder, verbose=False)

    # Вычисление значения полинома Эрмита
    result_hermite = get_hermite_value(table, level_of_polynomial, x_finder, verbose=True)  # Используем функцию get_hermite_value

    # Вывод результатов
    print('Результат полученный при помощи полинома Ньютона: {:10.5f}\nРезультат полученный при помощи полинома Эрмита:'
          ' {:10.5f}'.format(result_newton, result_hermite))


def get_table_with_more_levels():
    table = read_point_table(FILE_TABLE_1)  # Используем функцию read_point_table
    x_values, y_values, y_derivative = table[0], table[1], table[2]
    level_of_polynomial = [2, 5, 8, 11]
    x_finder = float(input("Введите X для подсчета значения: "))
    print_header_of_table(x_finder)
    for i in level_of_polynomial:
        result_newton = get_newton_value(table, i, x_finder, verbose=False)
        result_hermite = get_hermite_value(table, i, x_finder)  # Используем функцию get_hermite_value
        print_row_of_table(i, result_newton, result_hermite)


def find_root_with_newton_polynomial(level_of_polynomial, x_values, y_values, table):
    low, high = x_values[0], x_values[-1]
    while high - low > 1e-6:
        middle = (low + high) / 2
        value = get_newton_value(table, level_of_polynomial, middle, verbose=False)
        if value > 0:
            high = middle
        else:
            low = middle
    return (low + high) / 2


def find_root_with_hermite_polynomial(level_of_polynomial, low, high, table):
    while high - low > 1e-6:
        middle = (low + high) / 2
        value = get_hermite_value(table, level_of_polynomial, middle)  # Используем функцию get_hermite_value
        if value > 0:
            high = middle
        else:
            low = middle
    return (low + high) / 2


def find_roots():
    level_of_polynomial = int(input("Введите степень полинома для поиска: "))
    table = read_point_table(FILE_TABLE_1)  # Используем функцию read_point_table
    x_values, y_values, y_derivative = table[0], table[1], table[2]
    result_newton = find_root_with_newton_polynomial(level_of_polynomial, x_values, y_values, table)
    result_hermite = find_root_with_hermite_polynomial(level_of_polynomial, x_values[0], x_values[-1], table)
    print('Корень полученный при помощи полинома Ньютона: {:10.5f}\nКорень полученный при помощи полинома Эрмита: '
          '{:10.5f}'.format(result_newton, result_hermite))


def find_roots_equation(table1, table2):
    roots = []
    flag = 0
    arr = table1[0] + table2[0]
    x_min = min(arr)
    n1 = len(table1) - 1
    n2 = len(table2) - 1

    while flag != 1:
        x_min += 0.00001
        y1 = get_newton_value(table1, n1, x_min, verbose=False)
        y2 = get_newton_value(table2, n2, x_min, verbose=False)
        if abs(y1 - y2) < 1e-4:
            roots.append((x_min, (y1 + y2) / 2))
            flag = 1
    return roots


def find_equation():
    table1 = [[], []]
    read_from_file(table1, FILE_TABLE_2)
    table2 = [[], []]
    read_from_file(table2, FILE_TABLE_3)
    roots = find_roots_equation(table1, table2)

    print("|---------------------------|")
    print("|  №  |     X    |     Y    |")
    print("|---------------------------|")
    for i in range(len(roots)):
        print("|{:5d}|{:10.5f}|{:10.5f}|".format(i, roots[i][0], roots[i][1]))
        print("|---------------------------|")
