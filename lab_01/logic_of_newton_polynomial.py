def get_nearest_index(point_table, x):
    """
    Находит индекс ближайшей точки к x.
    """
    diff = abs(point_table[0][0] - x)
    nearest_index = 0
    for i in range(len(point_table[0])):
        if abs(point_table[0][i] - x) < diff:
            diff = abs(point_table[0][i] - x)
            nearest_index = i
    return nearest_index


def get_config_table(point_table, n, x):
    """
    Формирует конфигурационную таблицу для интерполяции.
    """
    low = high = get_nearest_index(point_table, x)
    for i in range(n):
        if i % 2 != 0:
            if low == 0:
                high += 1
            else:
                low -= 1
        else:
            if high == len(point_table[0]) - 1:
                low -= 1
            else:
                high += 1

    low = max(0, low)
    high = min(len(point_table[0]) - 1, high)

    return [point_table[0][low:high + 1], point_table[1][low:high + 1]]


def init_newton_diff_table(x_list, y_list):
    """
    Инициализирует таблицу разностей для полинома Ньютона.
    """
    return [x_list, y_list]


def fill_newton_diff_table(diff_table):
    """
    Заполняет таблицу разделённых разностей для полинома Ньютона.
    """
    length = len(diff_table[0])
    for i in range(1, length):
        new_y_list = []
        curr_y_list = diff_table[i]
        for j in range(length - i):
            new_y = (curr_y_list[j] - curr_y_list[j + 1]) / (diff_table[0][j] - diff_table[0][j + i])
            new_y_list.append(new_y)
        diff_table.append(new_y_list)
    return diff_table


def get_value_by_diff_table(diff_table, x):
    """
    Вычисляет значение полинома Ньютона в точке x по таблице разностей.
    """
    res_value = diff_table[1][0]
    curr_x = 1
    x_list = diff_table[0]
    for i in range(2, len(diff_table)):
        curr_y = diff_table[i][0]
        curr_x *= x - x_list[i - 2]
        res_value += curr_x * curr_y
    return res_value


def get_newton_value(point_table, n, x, verbose=False):
    """
    Вычисляет значение полинома Ньютона в точке x.
    """
    config_table = get_config_table(point_table, n, x)
    diff_table = init_newton_diff_table(config_table[0], config_table[1])
    fill_newton_diff_table(diff_table)
    if verbose:
        print("\nТаблица разделенных разностей (полином Ньютона)")
        print_diff_table(diff_table)
    return get_value_by_diff_table(diff_table, x)


def print_diff_table(diff_table):
    """
    Выводит таблицу разделённых разностей.
    """
    length = len(diff_table)
    print_separator(length, 7)
    print("|{:^7s}|{:^7s}".format("x", "y"), end='')
    for i in range(2, length):
        print("|{:^7s}".format("y" + "*" * (i - 1)), end='')
    print("|")
    print_separator(length, 7)
    for i in range(length - 1):
        for j in range(length):
            if j >= length - i:
                print("|{:^7s}".format(" "), end='')
            else:
                print("|{:^7.3f}".format(diff_table[j][i]), end='')
        print("|")
    print_separator(length, 7)
    print("")


def print_separator(length, step):
    """
    Выводит разделитель для таблицы.
    """
    print("+" + ("-" * step + "+") * length)
