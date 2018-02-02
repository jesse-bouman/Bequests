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


def mobility_matrix(gen, prev_gen, measure='w'):
    """
    Create a mobility matrix. Links for every person its current
    decile to the decile of its parents, and defines the transition
    probability for every possible combination parent decile ->
    child decile.

    :param gen: generation under research
    :type gen: Generation
    :param prev_gen: parent generation of generation under research
    :type gen: Generation
    :return: mobility matrix. Rows denote parent decile, columns
        denote child decile
    :rtype: numpy.array
    """
    # assign deciles to both generations
    gen.assign_deciles(measure=measure)
    prev_gen.assign_deciles(measure=measure)
    mm = np.zeros([10, 10])
    #for each couple in the current generation:
    for couple in gen.cs:
        # find the couple decile
        c_dec = couple.decile - 1

        # find the husband's parent decile
        parent_hb = couple.hb.pci
        p_hb_dec = prev_gen[parent_hb].decile - 1

        # find the wife's parent decile
        parent_wf = couple.wf.pci
        p_wf_dec = prev_gen[parent_wf].decile - 1

        # add
        mm[p_hb_dec, c_dec] = mm[p_hb_dec, c_dec] + 1
        mm[p_wf_dec, c_dec] = mm[p_wf_dec, c_dec] + 1
    mm  = mm / (gen.n * 2)
    return mm
