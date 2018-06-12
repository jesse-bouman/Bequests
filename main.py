import os

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import ks_2samp

from bequestlib.couple import Couple
from bequestlib.generation import Generation
from bequestlib.globals import OUTFOLDER
from bequestlib.metrics import lorentz_curve, gini
from bequestlib.output_preparation import ThesisPlotter
from bequestlib.person import Person
from bequestlib.society_rules import (all_children_equal, male_primogeniture, love_is_blind,
                                      best_partner_is_richest_partner)
from bequestlib.interactive_plotting import agg_to_plotly


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
        hb.add_inheritance(0.01)
        wf.add_inheritance(0.)
        cp = Couple(husband=hb, wife=wf, c_id=i)
        couples_list.append(cp)

    gen_1 = Generation(g_id=1, couples=couples_list)
    return gen_1


def next_gen_generator(bequest_rule, marital_tradition, tax_rate):
    adult_gen = init_generation()
    wealths = np.sort(adult_gen.to_array()[:, 1])
    a = wealths / sum(wealths)
    test_period = 0
    tot_period = 0
    while test_period < 3 and tot_period < 40:
        adult_gen.distribute_children()
        next_gen = adult_gen.produce_new_generation(bequest_rule=bequest_rule,
                                                    marital_tradition=marital_tradition,
                                                    tax_rate=tax_rate)
        adult_gen = next_gen

        wealth = np.sort(adult_gen.to_array()[:, 1])
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

    data = dict()
    for i in range(6):
        rate = i / 5
        mar_gen_i = next_gen_generator(all_children_equal, best_partner_is_richest_partner, rate)
        tmp_i = [dict(generation=adult_gen, ks_d=d, ks_p=p) for adult_gen, d, p in mar_gen_i]
        data[rate] = tmp_i

    plotter = ThesisPlotter(data)
    plotter.fig_lorentz_per_tax_rate()

    # res = (lorentz_curve(adult_gen) for adult_gen, d, p in tmp3)
    #plot_convergence_lorentz_curve(*res)
    # ds = [d for adult_gen, d, p in tmp]
    # ps = [p for adult_gen, d, p in tmp]


    """
    plt.clf()
    plt.axhline(y=0.5, color='orange')
    plt.plot(ps)
    plt.xlabel("Generation")
    plt.ylabel("p-value distribution equality")
    plt.savefig("P-value_ks_stat"+TIMESTAMP+".png")

    plt.clf()
    plt.plot(res2)
    plt.xlabel("generation")
    plt.ylabel("Gini coefficient")
    plt.savefig("gini_" + TIMESTAMP + ".png")
    """


if __name__ == '__main__':
    main()

