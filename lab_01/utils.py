def read_from_file(table, filename):
    with open(file=filename, mode='r') as file:
        file.readline()
        for line in file:
            table.append(list(map(float, line.split())))
