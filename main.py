import os

from bequestlib.couple import Couple
from bequestlib.generation import Generation
from bequestlib.globals import OUTFOLDER
from bequestlib.metrics import lorentz_curve, gini, mobility_matrix
from bequestlib.person import Person
from bequestlib.society_rules import (all_children_equal,
                                      love_is_blind)
from bequestlib.output_preparation import plot_lorentz_curve, plot_mobility_matrix
import matplotlib.pyplot as plt
import numpy as np

def init_generation():
    # set up a fully egalitarian starting generation
    n = 3000
    couples = int(n / 2.)
    couples_list = []
    for i in range(couples):
        hb = Person(gender=True, parent_couple_id=i)
        wf = Person(gender=False, parent_couple_id=couples-i)
        hb.set_id(i)
        wf.set_id(couples+i)
        hb.add_inheritance(100)
        wf.add_inheritance(100)
        cp = Couple(husband=hb, wife=wf, c_id=i)
        couples_list.append(cp)

    gen_1 = Generation(g_id=1, couples=couples_list)
    return gen_1


def main():
    if not os.path.exists(OUTFOLDER):
        os.mkdir(OUTFOLDER)
    os.chdir(OUTFOLDER)

    adult_gen = init_generation()

    for t in range(100):
        adult_gen.distribute_children()
        next_gen = adult_gen.produce_new_generation(bequest_rule=all_children_equal,
                                                    marital_tradition=love_is_blind)
        prev_gen = adult_gen
        adult_gen = next_gen
        x, y = lorentz_curve(adult_gen)
        gin = gini(x, y)

    plot_mobility_matrix(mobility_matrix(adult_gen, prev_gen))
    plot_lorentz_curve(y)


    plt.show()

if __name__ == '__main__':
    main()

