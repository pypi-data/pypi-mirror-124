import numpy as np
import matplotlib.pyplot as plt

from typing import List, Tuple, Union

def fast_hist(array: List[Union[int, float]],
              bins: int) -> Tuple[List[int], List[float]]:
    """
    Builds bins' labels and bins' value counts for given array
    :param array: array with numeric values
    :param bins:  number of bins in result distribution
    :return: Two lists:
             first contains value counts of each bin,
             second contains list of bins' labels
    """
    array = np.array(array)
    left = array.min()
    right = array.max()
    step = (right - left) / bins
    if step == 0.:
        step = 0.1

    as_indices = np.clip(((array - left) / step).astype(int),
        0,
        bins - 1)
    values, value_cnts = np.unique(as_indices, return_counts=True)

    res_y = np.zeros(bins, dtype=int)
    res_y[values] = value_cnts

    return res_y, np.linspace(left, right, bins + 1)

def fast_hist_show(array: List[Union[int, float]], bins: int):
    res_y, res_x = fast_hist(array, bins)
    plt.bar(res_x[:-1], res_y, 1. / (bins * 1.2))