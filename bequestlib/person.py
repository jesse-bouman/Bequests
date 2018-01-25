import numpy as np
from globals import NU, GAMMA, E_S, P, G
import matplotlib.pyplot as plt

class Person:
    """

    """
    def __init__(self, gender, parent_couple_id):
        """

        :param gender:
        :param parent_couple_id:
        """
        self.g = gender
        self.inh = 0
        self.id = None
        self.pci = parent_couple_id

    def add_inheritance(self, inheritance):
        """

        :param inheritance:
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







