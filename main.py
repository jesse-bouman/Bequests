import os

from bequestlib.couple import Couple
from bequestlib.generation import Generation
from bequestlib.globals import OUTFOLDER
from bequestlib.metrics import lorentz_curve, gini, mobility_matrix
from bequestlib.person import Person
from bequestlib.society_rules import (all_children_equal,
                                      love_is_blind, best_partner_is_richest_partner)
from bequestlib.output_preparation import plot_lorentz_curve, plot_mobility_matrix
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import ks_2samp

def init_generation():
    # set up a fully egalitarian starting generation
    n = 10000
    couples = int(n / 2.)
    couples_list = []
    for i in range(couples):
        hb = Person(gender=True, parent_couple_id=i)
        wf = Person(gender=False, parent_couple_id=couples-i)
        hb.set_id(i)
        wf.set_id(couples+i)
        hb.add_inheritance(0)
        wf.add_inheritance(0)
        cp = Couple(husband=hb, wife=wf, c_id=i)
        couples_list.append(cp)

    gen_1 = Generation(g_id=1, couples=couples_list)
    return gen_1

def asf_generator():
    adult_gen = init_generation()
    wealths = np.sort(adult_gen.to_array()[:, 1])
    a = wealths / sum(wealths)
    test_period = 0
    while test_period < 6:
        adult_gen.distribute_children()
        next_gen = adult_gen.produce_new_generation(bequest_rule=all_children_equal,
                                                    marital_tradition=best_partner_is_richest_partner)
        prev_gen = adult_gen
        adult_gen = next_gen
        x, y = lorentz_curve(adult_gen)

        wealths = np.sort(adult_gen.to_array()[:, 1])
        prev_a = a
        a = wealths / sum(wealths)
        d, p = ks_2samp(prev_a, a)
        if p > 0.5:
            test_period = test_period + 1
        else:
            test_period = 0
        yield adult_gen


def main():
    if not os.path.exists(OUTFOLDER):
        os.mkdir(OUTFOLDER)
    os.chdir(OUTFOLDER)

    res = [lorentz_curve(adult_gen) for adult_gen in asf_generator()]
    res2 = [gini(*y) for y in res]
    plt.plot(res2)
    plt.show()

if __name__ == '__main__':
    main()

