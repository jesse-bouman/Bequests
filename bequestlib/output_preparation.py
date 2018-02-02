import matplotlib.pyplot as plt
import numpy as np
from bequestlib.globals import TIMESTAMP

def plot_lorentz_curve(y):
    """

    :param y:
    :return:
    """
    X = np.linspace(0, 1, len(y))
    plt.xlabel("perc of pop")
    plt.ylabel('perc of wealth')
    plt.plot(X, y, X, X)
    axes = plt.gca()
    axes.set_ylim([0, 1])
    plt.show()


def plot_mobility_matrix(mm):
    """
    Plot the mobility matrix *mm* to a normalized table in png format.
    Shows probability information both written in percentages, and by
    applying a colour map to the cells.

    :param mm: Mobility matrix, containing probabilities of a child
        with parents in row i, ending up in column j.
    :type mm: numpy.array
    """
    fig, axs = plt.subplots(1, 1)
    axs.axis('tight')
    axs.axis('off')
    cmm = mm/np.max(mm)
    rows = range(1,11)
    tmm = (mm*100).tolist()
    tmm = [map("{:.2f}%".format, row) for row in tmm]
    axs.table(cellText=tmm, loc='center',
              cellColours=plt.cm.BuPu(cmm), rowLabels=rows,
              colLabels=rows)
    plt.savefig("mobility_matrix"+TIMESTAMP+'.png')