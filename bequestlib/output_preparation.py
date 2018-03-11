import matplotlib.pyplot as plt
import numpy as np
from bequestlib.globals import TIMESTAMP
from matplotlib.animation import FuncAnimation

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


def plot_convergence_lorentz_curve(*args):
    """
    Make an animated GIF file showing the convergence of subsequent
    Lorentz curves.

    :param args: x, y pairs of Lorentz curves to be outputted
    :type args: tuple of tuple of array-like
    """
    print(args)
    fig, ax = plt.subplots()
    fig.set_tight_layout(True)

    # Query the figure's on-screen size and DPI. Note that when saving the figure to
    # a file, we need to provide a DPI for that separately.
    print('fig size: {0} DPI, size in inches {1}'.format(
        fig.get_dpi(), fig.get_size_inches()))

    x = args[0][0]

    def update(i):
        label = 'timestep {0}'.format(i)
        print(label)
        ax.clear()
        y = args[i][1]
        ax.set_xlabel(label)
        ax.plot(x, x)
        ax.plot(x, y)

    # FuncAnimation will call the 'update' function for each frame; here
    # animating over 10 frames, with an interval of 200ms between frames.
    anim = FuncAnimation(fig, update, frames=len(args), interval=200)
    anim.save("convergence_Lorentz_"+TIMESTAMP+".gif", dpi=80, writer='imagemagick')

