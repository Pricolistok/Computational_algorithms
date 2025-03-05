def read_point_table(filename):
    point_table = [[], [], [], []]
    with open(filename) as f:
        for line in f.readlines():
            point_list = list(map(float, line.split()))
            point_table[0].append(point_list[0])
            point_table[1].append(point_list[1])
            point_table[2].append(point_list[2])
            point_table[3].append(point_list[3])
    return point_table


def read_from_file(table, filename):
    with open(file=filename, mode='r') as file:
        for line in file:
            x, y = map(float, line.split())
            table[0].append(x)
            table[1].append(y)
