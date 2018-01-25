from globals import NU, GAMMA, E_S, G
import numpy as np
from bequestlib.person import Person


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
        self.optimize_utility()
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
        b = (1 + G) * GAMMA * w
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
