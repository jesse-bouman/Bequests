from bequestlib.person import Person, Couple, Generation
import numpy as np
import matplotlib.pyplot as plt
# set up a fully egalitarian starting generation



def bequestrule(children, b):
    return [b/len(children)]*len(children)


def oldest_gets_all(children, b):
    return [b] + [0.]*(len(children)-1)


def best_partner_is_richest_partner(bachelor_stats, bachelorette_stats):
    order_bach = bachelor_stats[:, -1].argsort()
    order_bachts = bachelorette_stats[:, -1].argsort()
    groom_order = bachelor_stats[order_bach][:,0]
    bride_order = bachelorette_stats[order_bachts][:, 0]
    return groom_order.astype(int), bride_order.astype(int)


def love_is_blind(bachelor_stats, bachelorette_stats):
    b_ids = bachelor_stats[:, 0]
    np.random.shuffle(b_ids)
    groom_order = b_ids
    bride_order = bachelorette_stats[:, 0]
    return groom_order.astype(int), bride_order.astype(int)


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
adult_gen = gen_1

for t in range(100):
    adult_gen.distribute_children()
    next_gen = adult_gen.produce_new_generation(bequest_rule=oldest_gets_all,
                                                marital_tradition=best_partner_is_richest_partner)
    adult_gen = next_gen
    adult_gen.lorentz_curve()
    print(adult_gen.gini)

y = adult_gen.y
X = np.linspace(0, 1, len(y))
plt.xlabel("perc of pop")
plt.ylabel('perc of wealth')
plt.plot(X, y, X, X)
axes = plt.gca()
axes.set_ylim([0, 1])
plt.show()
