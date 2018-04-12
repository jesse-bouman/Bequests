import os

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import ks_2samp

from bequestlib.couple import Couple
from bequestlib.generation import Generation
from bequestlib.globals import OUTFOLDER
from bequestlib.metrics import lorentz_curve, gini
from bequestlib.output_preparation import plot_convergence_lorentz_curve
from bequestlib.person import Person
from bequestlib.society_rules import (all_children_equal, male_primogeniture, love_is_blind,
                                      best_partner_is_richest_partner)


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
    mar_gen_0 = next_gen_generator(all_children_equal, best_partner_is_richest_partner, 0)
    mar_gen_2 = next_gen_generator(all_children_equal, best_partner_is_richest_partner, 0.2)
    mar_gen_4 = next_gen_generator(all_children_equal, best_partner_is_richest_partner, 0.4)
    mar_gen_6 = next_gen_generator(all_children_equal, best_partner_is_richest_partner, 0.6)
    mar_gen_8 = next_gen_generator(all_children_equal, best_partner_is_richest_partner, 0.8)
    mar_gen_10 = next_gen_generator(all_children_equal, best_partner_is_richest_partner, 1)
    tmp_1 = [(adult_gen, d, p) for adult_gen, d, p in mar_gen_0]
    tmp_2 = [(adult_gen, d, p) for adult_gen, d, p in mar_gen_2]
    tmp_3 = [(adult_gen, d, p) for adult_gen, d, p in mar_gen_4]
    tmp_4 = [(adult_gen, d, p) for adult_gen, d, p in mar_gen_6]
    tmp_5 = [(adult_gen, d, p) for adult_gen, d, p in mar_gen_8]
    tmp_6 = [(adult_gen, d, p) for adult_gen, d, p in mar_gen_10]

    e1 = tmp_1[-1][0].time_spent_working()
    e2 = tmp_2[-1][0].time_spent_working()
    e3 = tmp_3[-1][0].time_spent_working()
    e4 = tmp_4[-1][0].time_spent_working()
    e5 = tmp_5[-1][0].time_spent_working()
    e6 = tmp_6[-1][0].time_spent_working()

    plt.plot([0, 20, 40, 60, 80, 100], [e1, e2, e3, e4, e5, e6])
    plt.xlabel('Tax Rate (%)')
    plt.ylabel('Total labour supply')
    plt.show()
    plt.clf()
    # res = (lorentz_curve(adult_gen) for adult_gen, d, p in tmp3)
    #plot_convergence_lorentz_curve(*res)
    # ds = [d for adult_gen, d, p in tmp]
    # ps = [p for adult_gen, d, p in tmp]

    plt.clf()
    x1, y1 = lorentz_curve(tmp_1[-1][0])
    x2, y2 = lorentz_curve(tmp_2[-1][0])
    x3, y3 = lorentz_curve(tmp_3[-1][0])
    x4, y4 = lorentz_curve(tmp_4[-1][0])
    x5, y5 = lorentz_curve(tmp_5[-1][0])
    x6, y6 = lorentz_curve(tmp_6[-1][0])

    gini_1 = gini(x1, y1)
    gini_2 = gini(x2, y2)
    gini_3 = gini(x3, y3)
    gini_4 = gini(x4, y4)
    gini_5 = gini(x5, y5)
    gini_6 = gini(x6, y6)

    plt.plot([0, 20, 40, 60, 80, 100], [gini_1, gini_2, gini_3, gini_4, gini_5, gini_6])
    plt.xlabel('Tax Rate (%)')
    plt.ylabel('GINI coefficient')
    plt.show()
    plt.clf()

    plt.plot(x1, y1, label='tax rate 0%')
    plt.plot(x2, y2, label='tax rate 20%')
    plt.plot(x3, y3, label='tax rate 40%')
    plt.plot(x4, y4, label='tax rate 60%')
    plt.plot(x5, y5, label='tax rate 80%')
    plt.plot(x6, y6, label='tax rate 100%')
    plt.legend()
    plt.savefig('compare_rules.png')
    plt.show()
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

