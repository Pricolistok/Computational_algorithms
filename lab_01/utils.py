from settings import FILE_TABLE


def read_from_file(table):
    with open(file=FILE_TABLE, mode='r') as file:
        file.readline()
        for line in file:
            table.append(list(map(float, line.split())))
