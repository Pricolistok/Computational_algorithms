def get_nearest_index(point_table, x):
    diff = abs(point_table[0][0] - x)
    nearest_index = 0
    for i in range(len(point_table[0])):
        if abs(point_table[0][i] - x) < diff:
            diff = abs(point_table[0][i] - x)
            nearest_index = i
    return nearest_index


def get_config_table(point_table, n, x, is_hermit):
    low = high = get_nearest_index(point_table, x)
    limit = n
    start = 0
    if is_hermit:
        limit = (n + 1) // 2 - n % 2
        start = 0
    for i in range(start, limit):
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

    num_sublists = len(point_table)
    if num_sublists == 4:
        return [point_table[0][low:high + 1], point_table[1][low:high + 1], point_table[2][low:high + 1], point_table[3][low:high + 1]]
    elif num_sublists == 3:
        return [point_table[0][low:high + 1], point_table[1][low:high + 1], point_table[2][low:high + 1]]


def init_hermite_diff_table(x_list, y_list, n, is_backward):
    diff_table = [[xi for x in x_list for xi in [x, x]],
                  [yi for y in y_list for yi in [y, y]]]
    if is_backward:
        diff_table = [[yi for y in y_list for yi in [y, y]],
                      [xi for x in x_list for xi in [x, x]]]
    if (n + 1) % 2 != 0:
        diff_table[0].pop()
        diff_table[1].pop()
    return diff_table


def fill_hermite_diff_table(diff_table, derivatives, second_derivatives):
    length = len(diff_table[0])
    for i in range(1, length):
        new_y_list = []
        curr_y_list = diff_table[i]
        for j in range(length - i):
            x_diff = diff_table[0][j] - diff_table[0][j + i]
            if x_diff == 0 and i == 1:
                new_y = derivatives[j // 2]
            elif x_diff == 0 and i == 2:
                new_y = second_derivatives[j // 2] / 2
            else:
                new_y = (curr_y_list[j] - curr_y_list[j + 1]) / x_diff
            new_y_list.append(new_y)
        diff_table.append(new_y_list)
    return diff_table


def get_value_by_diff_table(diff_table, x):
    res_value = diff_table[1][0]
    curr_x = 1
    x_list = diff_table[0]
    for i in range(2, len(diff_table)):
        curr_y = diff_table[i][0]
        curr_x *= x - x_list[i - 2]
        res_value += curr_x * curr_y
    return res_value


def get_hermite_value(point_table, n, x, verbose=False):
    config_table = get_config_table(point_table, n, x, True)
    diff_table = init_hermite_diff_table(config_table[0], config_table[1], n, False)
    fill_hermite_diff_table(diff_table, config_table[2], config_table[3])
    if verbose:
        print("\nТаблица разделенных разностей (полином Эрмита)")
        print_diff_table(diff_table)
    return get_value_by_diff_table(diff_table, x)


def print_diff_table(diff_table):
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
    print("+" + ("-" * step + "+") * length)