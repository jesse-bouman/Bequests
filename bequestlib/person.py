import numpy as np
from globals import NU, GAMMA, E_S


class Person:
    """

    """
    def __init__(self, gender, parent_couple_id):
        """

        :param gender:
        :param bequest:
        """
        self.g = gender
        self.inh = 0
        self.id = None
        self.pci = parent_couple_id

    def add_inheritance(self, inheritance):
        """

        :param inheritance:
        :return:
        """
        self.inh = self.inh + inheritance

    def set_id(self, p_id):
        self.id = p_id

    def to_array(self):
        return [self.id, int(self.g), self.pci, self.inh]

    def __str__(self):
        g_dict = {True: "Male", False: "Female"}
        string = """Person {}, {} \nParent couple id {} \nInherited {}
                 """.format(self.id, g_dict[self.g], self.pci, self.inh)
        return string

    def __repr__(self):
        return self.__str__()


class Couple:
    """

    """
    def __init__(self, husband, wife, c_id):
        self.hb = husband
        self.wf = wife
        self.inh_wealth = self.hb.inh + self.wf.inh
        self.children = []
        self.e = None
        self.w = None
        self.c = None
        self.b = None
        self.id = c_id

    def get_children(self, boys, girls):
        child_vector = [True]*boys + [False]*girls
        np.random.shuffle(child_vector)
        self.children = child_vector

    def optimize_utility(self):
        i = self.inh_wealth
        e = np.maximum((E_S - NU * i) / (1. + NU), 0)
        w = e + i
        c = (1 - GAMMA) * w
        b = (1 + GAMMA) * GAMMA * w
        self.e = e
        self.w = w
        self.c = c
        self.b = b


    def produce_new_adults(self, bequestrule):
        bequests = bequestrule(self.children, self.b)
        new_adults = []
        for i in range(len(self.children)):
            gender = self.children[i]
            inheritance = bequests[i]
            new_adult = Person(gender=gender, parent_couple_id=self.id)
            new_adult.add_inheritance(inheritance)
            new_adults.append(new_adult)
        return new_adults







class Generation:
    def __init__(self, g_id, couples):
        self.cs = couples
        self.id = g_id
        self.preg = self.population_register()
        
    def adult_population(self):
        men = []
        women = []
        for couple in self.cs:
            men.append(couple.hb)
            women.append(couple.wf)
        return men, women

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
        groom_order, bride_order = marital_tradition(bachelor_stats, bachelorette_stats)
        new_couples = []
        c_id = 1
        for i in range(len(groom_order)):
            groom = bachelors[groom_order[i]]
            bride = bachelorettes[bride_order[i]]
            new_couple = Couple(groom, bride, c_id)
            c_id += 1
            new_couples.append(new_couple)
        return Generation(self.id+1, new_couples)

    def produce_new_generation(self, bequest_rule, marital_tradition):
        bachelors, bachelorettes = self.produce_next_gen_bachelors(bequest_rule)
        new_gen = self.match_bachelors(bachelors, bachelorettes, marital_tradition)
        return new_gen

    def _dict_to_statslist(self, bach_dict):
        m = len(bach_dict.itervalues().next().to_array())
        bachelor_stats = np.zeros((len(bach_dict), m))
        i = 0
        for person in bach_dict.values():
            bachelor_stats[i, :] = person.to_array()
            i = i + 1
        return bachelor_stats


def bequestrule(children, b):
    return [b/len(children)]*len(children)


def best_partner_is_richest_partner(bachelor_stats, bachelorette_stats):

    groom_order = np.sort(bachelor_stats.T, axis=-1)[0, :]
    bride_order = np.sort(bachelorette_stats.T, axis=-1)[0, :]
    return groom_order.astype(int), bride_order.astype(int)


def love_is_blind(bachelor_stats, bachelorette_stats):
    b_ids = bachelor_stats[:, 0]
    np.random.shuffle(b_ids)
    groom_order = b_ids
    bride_order = bachelorette_stats[:, 0]
    return groom_order.astype(int), bride_order.astype(int)

h = Person(True, 0)
h.set_id(1)
w = Person(False, 1)
w.set_id(2)
h.add_inheritance(100)
w.add_inheritance(30)

h2 = Person(True, 0)
h2.set_id(3)
w2 = Person(False, 1)
w2.set_id(4)
h2.add_inheritance(100)
w2.add_inheritance(100)

c = Couple(husband=h, wife=w, c_id=0)
c2 = Couple(husband=h2, wife=w2, c_id=1)
g = Generation(1, [c, c2])
print c.inh_wealth
c.get_children(1, 2)
c2.get_children(1,0)
c.optimize_utility()
c2.optimize_utility()
reg = g.population_register()
b, bt = g.produce_next_gen_bachelors(bequestrule)
bs = g.match_bachelors(b, bt, love_is_blind)
g2 = g.produce_new_generation(bequestrule, best_partner_is_richest_partner)
print(g2.cs[1].inh_wealth)

