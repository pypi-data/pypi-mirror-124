import math
from matplotlib.container import BarContainer
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
    lower, upper = min(array), max(array)
    bucket_size = (upper - lower) / bins

    def bin_number(x):
        return min(math.floor((x - lower) / bucket_size), bins - 1)
    
    result = ([], [])
    for bin in range(0, bins):
        result[0].append(0)
        result[1].append(bin * bucket_size + lower)
    
    result[1].append(upper)
    for x in array:
        result[0][bin_number(x)] += 1
    return result

def my_hist(array: List[Union[int, float]], 
              bins: int) -> BarContainer:
    l = min(array)
    r = max(array)
    counts, labels = fast_hist(array, bins=bins)
    return plt.bar(labels[:-1], counts, width=(l - r)/bins)
