from scipy.optimize import curve_fit
import numpy as np

"""
Least squares method to calculate coefficient of increasing semantic orientation

"""


def linear_func(x, a0, a1):
    return a0 + a1 * x


def calulate_increase_1(y_data):
    # Initial guess.
    x0 = np.array([0.0, 0.0])
    x_data = np.arange(0, y_data.shape[0])
    a, cov_matrix = curve_fit(linear_func, x_data, y_data)
    return a


def calulate_increase_2(y_data):
    # Initial guess.
    x0 = np.array([0.0, 0.0])
    x_data = np.arange(0, y_data.shape[0])
    a, cov_matrix = curve_fit(linear_func, x_data, y_data)
    return a


if __name__ == '__main__':
    x_data = np.array([0.0, 1.0, 2.0, 3.0])
    y_data = np.array([0.1, 0.9, 2.2, 2.8])
    a, cov_matrix = curve_fit(linear_func, x_data, y_data)
    print(a)
