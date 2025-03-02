from logic_of_newton_polynomial import cnt_newton_polynomial
from logic_of_hermite_polynomial import cnt_hermite_interpolation
from utils import read_from_file
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
    table = []
    read_from_file(table, FILE_TABLE_1)
    x_values, y_values, y_derivative = [], [], []
    diff_data(table, x_values, y_values, y_derivative)
    level_of_polynomial = int(input("Введите степень полинома для нахождения значения: "))
    x_finder = float(input("Введите X для подсчета значения: "))
    result_newton = cnt_newton_polynomial(x_values, y_values, x_finder, level_of_polynomial)
    result_hermite = cnt_hermite_interpolation(table, level_of_polynomial, x_finder)
    print('Результат полученный при помощи полинома Ньютона: {:10.5f}\nРезультат полученный при помощи полинома Эрмита: {:10.5f}'.format(result_newton, result_hermite))


def get_table_with_more_levels():
    table = []
    read_from_file(table, FILE_TABLE_1)
    x_values, y_values, y_derivative = [], [], []
    diff_data(table, x_values, y_values, y_derivative)
    level_of_polynomial = list(map(int, input("Введите степени полинома для таблицы: ").split()))
    x_finder = float(input("Введите X для подсчета значения: "))
    print_header_of_table(x_finder)
    for i in level_of_polynomial:
        result_newton = cnt_newton_polynomial(x_values, y_values, x_finder, i)
        result_hermite = cnt_hermite_interpolation(table, i, x_finder)
        print_row_of_table(i, result_newton, result_hermite)


def find_root_with_newton_polynomial(level_of_polynomial, x_values, y_values):
    low, high = x_values[0], x_values[-1]
    while high - low > 1e-6:
        middle = (low + high) / 2
        value = cnt_newton_polynomial(x_values, y_values, middle, level_of_polynomial)
        if value > 0:
            high = middle
        else:
            low = middle
    return (low + high) / 2


def find_root_with_hermite_polynomial(level_of_polynomial, low, high, table):
    while high - low > 1e-6:
        middle = (low + high) / 2
        value = cnt_hermite_interpolation(table, level_of_polynomial, middle)
        if value > 0:
            high = middle
        else:
            low = middle
    return (low + high) / 2



def find_roots():
    level_of_polynomial = int(input("Введите степень полинома для поиска: "))
    table = []
    read_from_file(table, FILE_TABLE_1)
    x_values, y_values, y_derivative = [], [], []
    diff_data(table, x_values, y_values, y_derivative)
    result_newton = find_root_with_newton_polynomial(level_of_polynomial, x_values, y_values)
    result_hermite = find_root_with_hermite_polynomial(level_of_polynomial, x_values[0], x_values[-1], table)
    print('Корень полученный при помощи полинома Ньютона: {:10.5f}\nКорень полученный при помощи полинома Эрмита: {:10.5f}'.format(result_newton, result_hermite))


def find_roots_equation(table1, table2):
    roots = []
    x_val_1, y_val_1 = [i[1] for i in table1], [i[0] for i in table1]
    x_val_2, y_val_2 = [i[0] for i in table2], [i[1] for i in table2]
    x_min = min(x_val_2)
    x_max = max(x_val_2)
    x_values = [x_min + i * (x_max - x_min) / 1000 for i in range(1001)]  # Создаем 1000 точек между x_min и x_max

    table1 = [[row[1], row[0]] for row in table1]
    n1 = len(table1) - 1
    n2 = len(table2) - 1

    for x in x_values:
        y1 = cnt_newton_polynomial(x_val_1, y_val_1, x, n1)
        y2 = cnt_newton_polynomial(x_val_2, y_val_2, x, n2)
        if abs(y1 - y2) < 1e-3:
            roots.append((x, (y1 + y2)/2))
    return roots

def find_equation():
    table1 = []
    table2 = []
    read_from_file(table1, FILE_TABLE_2)
    read_from_file(table2, FILE_TABLE_3)

    roots = find_roots_equation(table1, table2)

    print("|---------------------------|")
    print("|  №  |     X    |     Y    |")
    print("|---------------------------|")
    for i in range(len(roots)):
        print("|{:5d}|{:10.5f}|{:10.5f}|".format(i, roots[i][0], roots[i][1]))
        print("|---------------------------|")