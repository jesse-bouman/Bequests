from bequestlib.globals import NU, GAMMA, E_S, G
import numpy as np
from bequestlib.model.person import Person

from bequestlib.random import get_random_state


class Couple:
    """
    Class defining a couple of man and woman with the ability to get children,
    optimize utility, work, consume and make bequests.
    """
    def __init__(self, husband, wife, c_id):
        """
        Class constructor, creating a couple with id *c_id* from a male and
        female person, *husband* and *wife* respectively. Initially the
        family has no children, and the couple hasn't made any decision within
        utility optimization yet

        :param husband: male counterpart of couple
        :type husband: Person
        :param wife: female counterpart of couple
        :type wife: Person
        :param c_id: couple identifier
        :type c_id: ``int``
        """
        self.hb = husband
        self.wf = wife
        self.inh_wealth = self.hb.inh + self.wf.inh
        self.children = []
        self.e = None
        self.w = None
        self.c = None
        self.b = None
        self.id = c_id
        self.decile = None

    def set_decile(self, decile):
        self.decile = decile

    def get_children(self, boys, girls):
        """
        Assign children to the family. Given a determined number of n *boys*
        and *m* girls, this method constructs a list of n+m booleans,
        containing n ``True`` for boys, and m ``False`` for girls. The list
        is randomly shuffled. The list order denotes order of birth: the eldest
        child is at index 0, the youngest at n + m - 1.

        Sets this array to the internal field ``children``

        :param boys: Number of sons in family
        :type boys: ``int``
        :param girls: Number of daughters in family
        :type girls: ``int``
        """
        child_vector = [True] * boys + [False] * girls
        random = get_random_state()
        random.shuffle(child_vector)
        self.children = child_vector

    def optimize_utility(self, mu_exp, tax_rate):
        """
        Let the couple, based on their total inherited wealth, make a utility
        optimizing decision on the amount of work, consumption and bequest they
        will spend within their lifetime.

        This method then assigns these decided quantities in the internal
        fields:

        | ``e``: Amount of time spent working
        | ``w``: Total acquired lifetime wealth
        | ``c``: lifetime consumption
        | ``b``: total funds available for bequests

        """
        i = self.inh_wealth
        k = len(self.children)
        perceived_w = (mu_exp * k) / ((1 + G) * (1 - tax_rate))
        e = np.maximum((E_S - NU * (i + perceived_w)) / (1. + NU), 0)
        w = e + i
        c = (1 - GAMMA) * (e + i + perceived_w)
        b = (1 + G) * GAMMA * (e + i + perceived_w) - (1 - GAMMA) / (1 - tax_rate) * mu_exp * k
        if b < 0:
            b = 0
            e = (1 - GAMMA - NU * i) / (1 - GAMMA + NU)
            c = (1 - GAMMA) / NU * (E_S - e)
        assert not b < 0
        assert not e < 0
        assert not e > 1
        assert not c < 0

        self.e = e
        self.w = w
        self.c = c
        self.b = b

    def produce_new_adults(self, bequestrule):
        """
        Turns the children of this couple into a list of new adults.
        Distributes the funds available for bequests among these children
        following *bequestrule*

        :param bequestrule: function that describes the rule by which this
                            family distributes its bequest amongst its
                            children.
        :type bequestrule: ``callable[list,float]``
        :return: list of persons without an id number yet, but with inherited
                 wealth from their parents.
        :rtype: ``list`` of ``Person``
        """
        bequests = bequestrule(self.children, self.b)
        new_adults = []
        for i in range(len(self.children)):
            gender = self.children[i]
            inheritance = bequests[i]
            new_adult = Person(gender=gender, parent_couple_id=self.id)
            new_adult.add_inheritance(inheritance)
            new_adults.append(new_adult)
        return new_adults

    def to_array(self):
        """
        Provide an array that represents the most important information
        of the couple object. Contains:

        * 0 : couple id
        * 1 : inherited wealth
        * 2 : total acquired wealth
        * 3 : time spent working

        :return: list of important couple stats
        :rtype: list
        """
        return [self.id, self.inh_wealth, self.w, self.e]
