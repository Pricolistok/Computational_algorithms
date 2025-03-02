def divided_diff(x_data, y_data):
    if len(y_data) == 1:
        return y_data[0]
    else:
        return (divided_diff(x_data[1:], y_data[1:]) - divided_diff(x_data[:-1], y_data[:-1])) / (
                    x_data[-1] - x_data[0])

def cnt_newton_polynomial(x_values, y_values, x, n):
    x_nodes = x_values[:n + 1]
    y_nodes = y_values[:n + 1]
    result = y_nodes[0]

    for i in range(1, n + 1):
        term = divided_diff(x_nodes[:i + 1], y_nodes[:i + 1])
        for j in range(i):
            term *= (x - x_nodes[j])
        result += term

    return result