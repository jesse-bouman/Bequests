import numpy as np
from bequestlib.couple import Couple
from bequestlib.globals import P


class Generation:
    def __init__(self, g_id, couples):
        self.cs = couples
        self.n = len(couples)
        self.id = g_id
        self.preg = self.population_register()
        self.gini = None
        self.x = self.y = None

    def adult_population(self):
        men = []
        women = []
        for couple in self.cs:
            men.append(couple.hb)
            women.append(couple.wf)
        return men, women

    def distribute_children(self):
        all_new_children = [True] * self.n + [False] * self.n
        np.random.shuffle(all_new_children)
        family_sizes = []
        i = 1
        j = 0
        for p in P:
            n_families_size_i = int(p * self.n)
            for fam in range(n_families_size_i):
                children = all_new_children[j: j +i]
                j = j + i
                family_sizes.append(children)
            i = i + 1
        np.random.shuffle(family_sizes)
        for i in range(self.n):
            children = family_sizes[i]
            boys = sum(children)
            girls = len(children) - boys
            self.cs[i].get_children(boys, girls)

    def population_register(self):
        reg = {}
        for couple in self.cs:
            for person in [couple.hb, couple.wf]:
                if person.id not in reg.keys() and person.id is not None:
                    reg[person.id] = person
                elif person.id is None:
                    raise Exception("""Cannot make population register with
                                       unregistered persons""")
                else:
                    raise Exception("""multiple persons in generation with 
                                       same id""")
        return reg

    def produce_next_gen_bachelors(self, bequest_rule):
        bachelors = {}
        bachelorettes = {}
        p_id = 1
        for couple in self.cs:
            new_adults = couple.produce_new_adults(bequest_rule)
            for new_adult in new_adults:
                new_adult.set_id(p_id)
                p_id += 1
                if new_adult.g:
                    bachelors[new_adult.id] = new_adult
                else:
                    bachelorettes[new_adult.id] = new_adult
        return bachelors, bachelorettes

    def match_bachelors(self, bachelors, bachelorettes, marital_tradition):

        bachelor_stats = self._dict_to_statslist(bachelors)
        bachelorette_stats = self._dict_to_statslist(bachelorettes)
        groom_order, bride_order = marital_tradition(bachelor_stats,
                                                     bachelorette_stats)
        new_couples = []
        c_id = 1
        for i in range(len(groom_order)):
            groom = bachelors[groom_order[i]]
            bride = bachelorettes[bride_order[i]]
            new_couple = Couple(groom, bride, c_id)
            c_id += 1
            new_couples.append(new_couple)
        return Generation(self.id + 1, new_couples)

    def produce_new_generation(self, bequest_rule, marital_tradition):
        bachelors, bachelorettes = self.produce_next_gen_bachelors(bequest_rule)
        new_gen = self.match_bachelors(bachelors, bachelorettes, marital_tradition)
        return new_gen


def lorentz_curve(gen):
    wealths = np.zeros((gen.n, 2))
    for i in range(len(gen.cs)):
        couple = gen.cs[i]
        wealths[i, 0] = 1
        wealths[i, 1] = couple.w
    wealths[:, 0] = wealths[:, 0 ] /np.sum(wealths[:, 0])
    wealths[:, 1] = wealths[:, 1] / np.sum(wealths[:, 1])
    sorted_arr = np.sort(wealths.T, axis=1).T
    x = np.cumsum(sorted_arr[:, 0])
    y = np.cumsum(sorted_arr[:, 1])
    mad = np.abs(np.subtract.outer(y, y)).mean()
    rmad = mad / np.mean(y)
    gini = 0.5 * rmad
    return x, y, gini


def _dict_to_statslist(bach_dict):
    m = len(bach_dict.itervalues().next().to_array())
    bachelor_stats = np.zeros((len(bach_dict), m))
    i = 0
    for person in bach_dict.values():
        bachelor_stats[i, :] = person.to_array()
        i = i + 1
    return bachelor_stats
