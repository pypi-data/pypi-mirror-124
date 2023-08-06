import matplotlib.pyplot as plt
from typing import List, Tuple, Union
import numpy as np


def get_plot(Ox, Oy):
    plt.plot(Ox, Oy)
    return plt.show()


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
    mx = max(array)
    mn = min(array)
    arr_bin = np.zeros(bins)
    dist = (mx - mn) / bins
    for ar in array:
        if ar == mx:
            arr_bin[bins - 1] += 1
        else:
            arr_bin[int((ar - mn) / dist)] += 1
    bin_val = np.array([int(x) for x in arr_bin])
    bin_name = np.linspace(mn, mx, bins)
    return (bin_val, bin_name)


__version__ = "1.0.6"
