from utils import read_from_file
from logic_of_newton_polynomial import cnt_newton_polynomial
from logic_of_hermite_polynomial import cnt_hermite_interpolation
from utils import read_from_file


def print_header_of_table(x: float):
    print(f"Данные при x = {x}")
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


def get_table():
    table = []
    read_from_file(table)
    x_values, y_values, y_derivative = [], [], []
    diff_data(table, x_values, y_values, y_derivative)
    read_from_file(table)
    level_of_polynomial = list(map(int, input("Введите степени полинома для таблицы: ").split()))
    x_finder = float(input("Введите X для подсчета значения: "))
    print_header_of_table(x_finder)
    for i in level_of_polynomial:
        result_newton = cnt_newton_polynomial(x_values, y_values, x_finder, i)
        result_hermite = cnt_hermite_interpolation(table, i, x_finder)
        print_row_of_table(i, result_newton, result_hermite)