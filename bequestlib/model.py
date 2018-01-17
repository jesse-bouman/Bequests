import numpy as np
import matplotlib.pyplot as plt
import math as m

n = 1000
p = [0.35, 0.45, 0.1, 0.06, 0.03, 0.01]
# p = [0.0, 1.0]
Es = 1
nu = 0.3
gamma = 0.4
g = m.pow(1.03, 25)

# starting division of bequests
B_0 = 100 * np.ones(n)
# B_0[:100] = 1000 * np.ones(100)
iterations = 50


def ChildrenVec(n, p):
    """
    test for doc

    :param n:
    :param p:
    :return:
    """
    # make k-child families
    k_fam = np.zeros(n)
    prev = 0
    for i in range(len(p)):
        nxt = prev + int(p[i] * n)
        k_fam[prev:nxt].fill(i + 1)
        prev = nxt

    # make index for each child
    indices = np.zeros(2 * n)
    last = 0
    for i in range(n):
        k = int(k_fam[i])
        for j in range(k):
            indices[last + j] = i
        last = last + k

    # assign gender to children randomly
    k_sons = np.copy(k_fam)
    k_daughters = np.zeros(n)

    female = np.zeros(2 * n)
    female[0:n].fill(1)
    np.random.shuffle(female)
    for i in range(2 * n):
        if female[i] == 1:
            j = int(indices[i])
            k_sons[j] = k_sons[j] - 1
            k_daughters[j] = k_daughters[j] + 1

    # assign random family size to families
    c = list(zip(k_sons, k_daughters, k_fam))
    np.random.shuffle(c)
    k_sons, k_daughters, k_fam = zip(*c)

    return k_fam, k_sons, k_daughters


def bequestRule(Bk, nsons, ndaughters):
    return Bk / (nsons + ndaughters)


def inherit(B, k_sons, k_daughters):
    i_women = np.zeros(n)
    i_men = np.zeros(n)

    ind = 0
    for i in range(n):
        ds = int(k_daughters[i])
        inher = bequestRule(B[i], k_sons[i], k_daughters[i])
        for k in range(ds):
            i_women[ind + k] = inher
        ind = ind + ds

    ind = 0
    for i in range(n):
        sons = int(k_sons[i])
        inher = bequestRule(B[i], k_sons[i], k_daughters[i])
        for k in range(sons):
            i_men[ind + k] = inher
        ind = ind + sons

    return i_men, i_women


def matchBachelors(i_men, i_women):
    i_men = np.sort(i_men)
    np.random.shuffle(i_women)
    return i_men + i_women


"""

def matchBachelors(i_men, i_women):
	i_men = np.sort(i_men)
	i_women = np.sort(i_women)
	return i_men + i_women
"""


def allocation(I_t):
    E_t = np.maximum((Es - nu * I_t) / (1. + nu), np.zeros(n))
    W_t = E_t + I_t
    C_t = (1 - gamma) * W_t
    B_t = (1 + g) * gamma * W_t
    return C_t, B_t, W_t


def gini(W):
    mad = np.abs(np.subtract.outer(W, W)).mean()
    rmad = mad / np.mean(W)
    g = 0.5 * rmad
    return g


def main():
    m = iterations
    Y = np.zeros(m)
    B_t = B_0
    for i in range(m):
        print "iteration = " + str(i)
        k_fam, k_sons, k_daughters = ChildrenVec(n, p)
        i_men, i_women = inherit(B_t, k_sons, k_daughters)
        It = matchBachelors(i_men, i_women)
        C_t, B_t, W_t = allocation(It)
        Y[i] = gini(W_t)
    s1 = W_t / np.sum(W_t)
    s1 = np.sort(s1)
    Lorenz = np.zeros(n)
    for i in range(n):
        Lorenz[i] = np.sum(s1[:i])
    print B_t
    X = np.linspace(0, 1, n)
    plt.xlabel("perc of pop")
    plt.ylabel('perc of wealth')
    plt.plot(X, Lorenz, X, X)
    plt.show()


main()
