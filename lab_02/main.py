import numpy as np

def newton_interpolation(x, y, xi):
    """Интерполяция полиномом Ньютона"""
    n = len(x)
    coef = np.zeros(n)
    for i in range(n):
        coef[i] = y[i]

    for j in range(1, n):
        for i in range(n - 1, j - 1, -1):
            coef[i] = (coef[i] - coef[i - 1]) / (x[i] - x[i - j])

    result = coef[-1]
    for i in range(n - 2, -1, -1):
        result = result * (xi - x[i]) + coef[i]

    return result

def tridiagonal_solve(A, d):
    """Решение трехдиагональной системы уравнений методом прогонки"""
    n = len(d)
    # Прямой ход метода прогонки
    for i in range(1, n):
        m = A[i][i - 1] / A[i - 1][i - 1]
        A[i][i] -= m * A[i - 1][i]
        d[i] -= m * d[i - 1]
    # Обратный ход метода прогонки
    x = np.zeros(n)
    x[-1] = d[-1] / A[-1][-1]
    for i in range(n - 2, -1, -1):
        x[i] = (d[i] - A[i][i + 1] * x[i + 1]) / A[i][i]
    return x

def cubic_spline_interpolation(x, y, xi):
    """Интерполяция кубическим сплайном"""
    n = len(x)
    h = np.diff(x)
    # Формирование системы уравнений для нахождения коэффициентов сплайна
    A = np.zeros((n, n))
    A[0, 0] = 1
    A[-1, -1] = 1
    for i in range(1, n - 1):
        A[i, i - 1] = h[i - 1]
        A[i, i] = 2 * (h[i - 1] + h[i])
        A[i, i + 1] = h[i]
    # Вектор правой части
    d = np.zeros(n)
    for i in range(1, n - 1):
        d[i] = 3 * ((y[i + 1] - y[i]) / h[i] - (y[i] - y[i - 1]) / h[i - 1])
    # Решение системы для нахождения коэффициентов c
    c = tridiagonal_solve(A, d)
    # Нахождение коэффициентов a, b, d
    a = y[:-1]
    b = np.zeros(n - 1)
    d_spline = np.zeros(n - 1)
    for i in range(n - 1):
        b[i] = (y[i + 1] - y[i]) / h[i] - h[i] * (2 * c[i] + c[i + 1]) / 3
        d_spline[i] = (c[i + 1] - c[i]) / (3 * h[i])
    # Поиск интервала, в который попадает xi
    idx = np.searchsorted(x, xi) - 1
    if idx < 0:
        idx = 0
    elif idx >= n - 1:
        idx = n - 2
    # Вычисление значения сплайна в точке xi
    dx = xi - x[idx]
    return a[idx] + b[idx] * dx + c[idx] * dx**2 + d_spline[idx] * dx**3

def read_data_from_file(filename):
    """Чтение данных из файла"""
    with open(filename, 'r') as file:
        lines = [line.strip() for line in file if line.strip()]

    z_vals = []
    f_values = []
    x_vals, y_vals = None, None

    index = 0
    while index < len(lines):
        if lines[index].startswith("z="):
            z_vals.append(float(lines[index].split("=")[1]))
            index += 1
        elif lines[index].startswith("y\\x"):
            if x_vals is None:
                x_vals = list(map(float, lines[index].split()[1:]))  # Считывание x
            index += 1
        elif lines[index][0].isdigit():  # Если строка начинается с числа, значит это данные
            matrix = []
            temp_y_vals = []
            while index < len(lines) and lines[index][0].isdigit():
                parts = list(map(float, lines[index].split()))
                temp_y_vals.append(parts[0])  # y-значения
                matrix.append(parts[1:])  # f(x, y) значения
                index += 1
            if y_vals is None:
                y_vals = temp_y_vals
            f_values.append(matrix)
        else:
            index += 1  # Пропускаем пустые строки или разделители

    # Преобразуем f_values в массив numpy
    # Убедимся, что все матрицы имеют одинаковую форму
    try:
        f_values = [np.array(f, dtype=float) for f in f_values]
    except ValueError as e:
        raise ValueError("Ошибка: данные в файле имеют неоднородную структуру. Проверьте файл.") from e

    return (
        np.array(x_vals, dtype=float),
        np.array(y_vals, dtype=float),
        np.array(z_vals, dtype=float),
        f_values  # Возвращаем список матриц для каждого z
    )

def interpolate_3d(x_vals, y_vals, z_vals, f_values, x, y, z, method='newton'):
    """Выполняет интерполяцию в трехмерном пространстве"""
    if len(f_values) == 0:
        raise ValueError("Ошибка: список f_values пуст. Проверьте структуру входных данных.")

    num_z = len(z_vals)
    interpolated_xy = []

    for i in range(num_z):
        f_xy = f_values[i]
        interpolated_x = []

        for row in f_xy:
            if method == 'newton':
                interpolated_x.append(newton_interpolation(x_vals, row, x))
            elif method == 'spline':
                interpolated_x.append(cubic_spline_interpolation(x_vals, row, x))
            else:
                raise ValueError("Неизвестный метод интерполяции. Используйте 'newton' или 'spline'.")

        if method == 'newton':
            interpolated_xy.append(newton_interpolation(y_vals, interpolated_x, y))
        elif method == 'spline':
            interpolated_xy.append(cubic_spline_interpolation(y_vals, interpolated_x, y))

    if method == 'newton':
        return newton_interpolation(z_vals, interpolated_xy, z)
    elif method == 'spline':
        return cubic_spline_interpolation(z_vals, interpolated_xy, z)

def mixed_interpolation(x_vals, y_vals, z_vals, f_values, x, y, z, method_x='newton', method_y='spline', method_z='newton'):
    if len(f_values) == 0:
        raise ValueError("Ошибка: список f_values пуст. Проверьте структуру входных данных.")

    num_z = len(z_vals)
    interpolated_xy = []

    for i in range(num_z):
        f_xy = f_values[i]
        interpolated_x = []

        for row in f_xy:
            if method_x == 'newton':
                interpolated_x.append(newton_interpolation(x_vals, row, x))
            elif method_x == 'spline':
                interpolated_x.append(cubic_spline_interpolation(x_vals, row, x))
            else:
                raise ValueError("Неизвестный метод интерполяции для x. Используйте 'newton' или 'spline'.")

        if method_y == 'newton':
            interpolated_xy.append(newton_interpolation(y_vals, interpolated_x, y))
        elif method_y == 'spline':
            interpolated_xy.append(cubic_spline_interpolation(y_vals, interpolated_x, y))

    if method_z == 'newton':
        return newton_interpolation(z_vals, interpolated_xy, z)
    elif method_z == 'spline':
        return cubic_spline_interpolation(z_vals, interpolated_xy, z)

data_file = "data.txt"
try:
    x_vals, y_vals, z_vals, f_values = read_data_from_file(data_file)
except ValueError as e:
    print(e)
else:
    if len(f_values) == 0:
        print("Ошибка: список f_values пуст. Проверьте входной файл.")
    else:
        try:
            x_target = float(input("Введите значение x_target: "))
            y_target = float(input("Введите значение y_target: "))
            z_target = float(input("Введите значение z_target: "))
        except ValueError:
            print("Ошибка: введены некорректные значения. Используйте числа.")
        else:
            method = input("Выберите метод интерполяции (newton, spline, mixed): ").strip().lower()
            if method == 'mixed':
                method_x = input("Выберите метод интерполяции по x (newton, spline): ").strip().lower()
                method_y = input("Выберите метод интерполяции по y (newton, spline): ").strip().lower()
                method_z = input("Выберите метод интерполяции по z (newton, spline): ").strip().lower()
                result = mixed_interpolation(x_vals, y_vals, z_vals, f_values, x_target, y_target, z_target, method_x, method_y, method_z)
            else:
                result = interpolate_3d(x_vals, y_vals, z_vals, f_values, x_target, y_target, z_target, method)

            print(f"Результат интерполяции для x={x_target}, y={y_target}, z={z_target}: {result}")