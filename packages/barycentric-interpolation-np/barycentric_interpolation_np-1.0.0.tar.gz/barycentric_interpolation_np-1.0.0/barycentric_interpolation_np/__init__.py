import numpy as np


def barycentric_interpolation(xs, ys):
    n = len(xs)
    w = np.ones((n,))

    for i in range(n):
        for j in range(n):
            if i != j:
                w[i] /= xs[i] - xs[j]

    def evaluate(x):
        result = 1
        up, down = 0, 0
        for i in range(n):
            if x == xs[i]:
                return ys[i]
            up += (w[i] / (x - xs[i])) * ys[i]
        for i in range(n):
            down += w[i] / (x - xs[i])

        result *= up / down
        return result

    return evaluate
