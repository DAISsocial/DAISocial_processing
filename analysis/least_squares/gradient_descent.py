import numpy as np


def linear_func(x, a0, a1):
    return a0 + a1 * x


def compute_gradients(X, Y, a):
    m = X.shape[0]
    return np.array([1 / m * sum([a[0] + a[1] * X[i[0]] - Y[i[0]]
                                  for i in enumerate(X)]),
                     1 / m * sum([(a[0] + a[1] * X[i[0]] - Y[i[0]]) * X[i[0]]
                                  for i in enumerate(X)])])


def gradient_descent(X, Y, learning_rate=0.001, nb_epochs=100000):
    iteration = 0

    a = np.array([0, 0])
    a_new = np.array([0, 0])
    while iteration < nb_epochs:
        params_grad = compute_gradients(X, Y, a_new)
        a, a_new = a_new, a_new - learning_rate * params_grad
        iteration += 1
    return a_new

if __name__ == '__main__':
    x_data = np.array([0.0, 1.0, 2.0, 3.0])
    y_data = np.array([0.9, 0.4, 0.3, 0.1])
    a = gradient_descent(x_data, y_data)
    print(a)

