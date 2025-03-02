def search_index(table, n, x):
    index = 0

    for line in table:
        if line[0] > x:
            break
        index += 1

    l_border = index - (n - n // 2)
    r_border = l_border + n

    if l_border < 0:
        l_border = 0
    elif r_border >= len(table):
        l_border = len(table) - n - 1

    return l_border


def compute_hermite_differences(nodes, n, index):
    differences = []
    for i in range(n + 1):
        differences.append([nodes[index + i][1]])

    for j in range(1, n + 1):
        for i in range(n + 1 - j):
            if j == 1 and nodes[index + i][0] == nodes[index + i + 1][0]:
                diff = nodes[index + i][2]  # Используем первую производную
            elif j == 2 and nodes[index + i][0] == nodes[index + i + 1][0]:
                diff = nodes[index + i][3]  # Используем вторую производную
            else:
                diff = (differences[i + 1][j - 1] - differences[i][j - 1]) / (nodes[index + i + j][0] - nodes[index + i][0])
            differences[i].append(diff)

    return differences


def table_extension(table):
    new_table = []
    for row in table:
        new_table.append(row)
        new_table.append(row)
        new_table.append(row)
    return new_table


def cnt_hermite_interpolation(table, level_inter, x):
    extended_table = table_extension(table)

    n = 3 * level_inter - 1
    index = search_index(extended_table, n, x)
    differences = compute_hermite_differences(extended_table, n, index)
    result = differences[0][0]
    for i in range(1, n + 1):
        term = differences[0][i]
        for j in range(i):
            term *= (x - extended_table[index + j][0])
        result += term

    return result

