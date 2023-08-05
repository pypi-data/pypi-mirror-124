from typing import List, Tuple, Union
import math
import numpy as np
from matplotlib import pyplot as plt


def fast_hist(array: List[Union[int, float]],
              bins: int) -> Tuple[List[int], List[float]]:
    min_element = max_element = array[0]
    size = len(array)
    for i in range(1, size):
        if array[i] > max_element:
            max_element = array[i]
        if array[i] < min_element:
            min_element = array[i]
    x = [float(0)] * bins
    x[0] = float(min_element)
    step = (max_element - min_element) / bins
    for i in range(1, bins):
        x[i] = float(x[i - 1] + step)

    y = [0] * bins
    for i in range(size):
        index = checker(min_element, step, array[i], bins)
        y[index] = y[index] + 1
    print(type(x[1]))
    return y, x


def checker(min_element, step, value, bins):
    answer = (value - min_element) / step
    answer = int(math.floor(answer))
    if answer == bins:
        answer = bins - 1
    return answer


def draw(array):
    value_counts, bins_names = fast_hist(array, len(set(array)))
    y_pos = np.arange(len(value_counts))
    plt.bar(y_pos, value_counts)
    plt.show()
    print('Значения колонок:', value_counts)
    print('Названия колонок:', bins_names)


draw([1, 1, 2, 3, 4, 1, 2, 3, 4])
