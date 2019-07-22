import os

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import ks_2samp

from bequestlib.model.couple import Couple
from bequestlib.model.generation import Generation
from bequestlib.globals import OUTFOLDER, N_POPULATION
from bequestlib.metrics.metrics import lorentz_curve
from bequestlib.model.person import Person
from bequestlib.model.society_rules import (all_children_equal, best_partner_is_richest_partner)


def init_generation():
    # set up a fully egalitarian starting generation
    n = N_POPULATION
    couples = int(n / 2.)
    couples_list = []
    for i in range(couples):
        hb = Person(gender=True, parent_couple_id=i)
        wf = Person(gender=False, parent_couple_id=couples-i)
        hb.set_id(i)
        wf.set_id(couples+i)
        hb.add_inheritance(0.01)
        wf.add_inheritance(0.)
        cp = Couple(husband=hb, wife=wf, c_id=i)

        couples_list.append(cp)

    gen_1 = Generation(g_id=1, couples=couples_list)
    gen_1.distribute_children()
    for cp in gen_1.cs:
        cp.optimize_utility(0, 0.0)
    return gen_1


def next_gen_generator(bequest_rule, marital_tradition, tax_rate):
    adult_gen = init_generation()
    wealths = np.sort(adult_gen.to_array()[:, 1])
    a = wealths / sum(wealths)
    test_period = 0
    tot_period = 0
    while test_period < 2 and tot_period < 100:

        next_gen = adult_gen.produce_new_generation(bequest_rule=bequest_rule,
                                                    marital_tradition=marital_tradition,
                                                    tax_rate=tax_rate)
        adult_gen = next_gen

        wealth = np.sort(adult_gen.to_array()[:, 2])
        prev_a = a
        a = wealth / sum(wealth)
        d, p = ks_2samp(prev_a, a)
        if p > 0.2:
            test_period = test_period + 1
        else:
            test_period = 0
        tot_period = tot_period + 1
        yield adult_gen, d, p


def main():
    if not os.path.exists(OUTFOLDER):
        os.mkdir(OUTFOLDER)
    os.chdir(OUTFOLDER)

    mar_gen_2 = next_gen_generator(all_children_equal, best_partner_is_richest_partner, 0.2)

    tmp_1 = [(adult_gen, d, p) for adult_gen, d, p in mar_gen_2]
    print([p for _, _, p in tmp_1])

    gen = tmp_1[-1][0]

    print(sum(c.b == 0 for c in gen.cs)/len(gen.cs))
    e_list = [c.e for c in gen.cs]
    w_list = [c.w for c in gen.cs]
    c_list = [c.c for c in gen.cs]
    lor = lorentz_curve(gen)
    # plot_stats(e_list, w_list, c_list, lor)


    # res = (lorentz_curve(adult_gen) for adult_gen, d, p in tmp3)
    #plot_convergence_lorentz_curve(*res)
    # ds = [d for adult_gen, d, p in tmp]
    # ps = [p for adult_gen, d, p in tmp]

    plt.clf()
    x1, y1 = lorentz_curve(tmp_1[-1][0])
    plt.plot(x1, y1)
    plt.show()



if __name__ == '__main__':
    main()

