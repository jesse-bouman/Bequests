import numpy as np


def lorentz_curve(gen):
    """
    Determine the lorentz curve for total wealth inequality of generation *gen*

    :param gen: generation of couples under research
    :type gen: Generation
    :return: x and y values of the lorentz curve
    :rtype: ``tuple`` of ``numpy.Array``
    """
    wealths = np.zeros((gen.n, 2))
    for i in range(len(gen.cs)):
        couple = gen.cs[i]
        wealths[i, 0] = 1
        wealths[i, 1] = couple.w
    wealths[:, 0] = wealths[:, 0] / np.sum(wealths[:, 0])
    wealths[:, 1] = wealths[:, 1] / np.sum(wealths[:, 1])
    sorted_arr = np.sort(wealths.T, axis=1).T
    x = np.cumsum(sorted_arr[:, 0])
    y = np.cumsum(sorted_arr[:, 1])

    return x, y


def gini(x, y):
    """
    calculate the GINI coefficient from the population's lorentz curve
    determined by *x* and *y*.

    :param x: x-values of Lorentz curve
    :type x: ``numpy.Array``
    :param y: y-values of the Lorentz curve
    :type y: ``numpy.Array``
    :return: GINI coefficient determined by Lorentz curve
    :rtype: ``float``
    """
    mad = np.abs(np.subtract.outer(y, y)).mean()
    rmad = mad / np.mean(y)
    gini = 0.5 * rmad
    return gini
