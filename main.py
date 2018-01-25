from bequestlib.person import Person
from bequestlib.couple import Couple
from bequestlib.generation import Generation
from bequestlib.metrics import lorentz_curve, gini
from bequestlib.society_rules import (oldest_gets_all,
                                      best_partner_is_richest_partner)
import numpy as np
import matplotlib.pyplot as plt


def init_generation():
    # set up a fully egalitarian starting generation
    n = 1000
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
    adult_gen = init_generation()

    for t in range(100):
        adult_gen.distribute_children()
        next_gen = adult_gen.produce_new_generation(bequest_rule=oldest_gets_all,
                                                    marital_tradition=best_partner_is_richest_partner)
        adult_gen = next_gen
        x, y = lorentz_curve(adult_gen)
        gin = gini(x, y)
        print(gin)

    X = np.linspace(0, 1, len(y))
    plt.xlabel("perc of pop")
    plt.ylabel('perc of wealth')
    plt.plot(X, y, X, X)
    axes = plt.gca()
    axes.set_ylim([0, 1])
    plt.show()


if __name__ == '__main__':
    main()

