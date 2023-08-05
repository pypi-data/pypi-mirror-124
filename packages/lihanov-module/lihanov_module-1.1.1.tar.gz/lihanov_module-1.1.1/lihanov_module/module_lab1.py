import numpy as np
import matplotlib.pyplot as plt

def simpleLagrange(rangeX, rangeY):
    if (len(rangeX) != len(rangeY)):
        raise ValueError("sizes of ranges must be equal")
    def getLi(x, xj):
        top = 1
        bot = 1
        for xi in rangeX:
            if (xi != xj):
                top *= x - xi
                bot *= xj - xi
        return top / bot
    def fun(x):
        res = 0
        for i in range(len(rangeY)):
            res += rangeY[i] * getLi(x, rangeX[i])
        return res
    return fun
    
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
    stop = max(array)
    start = min(array)
    step = (stop - start) / bins
    countArr = np.zeros(bins)
    for un in array:
        countArr[min(int((un - start) / step), bins - 1)] += 1
    binsNames = np.arange(start, stop, step)
    return (np.array([int(x) for x in countArr]), binsNames)