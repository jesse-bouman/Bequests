import numpy as np
from bequestlib.couple import Couple
from bequestlib.globals import P


class Generation:
    """
    Class defining a full generation of adult couples. Every generation's
    couples can procreate into a new generation, marrying following several
    marital rules, and bequeathing their wealth to their offspring following
    bequest rules.
    """
    def __init__(self, g_id, couples):
        """
        Constructor of a new generation with identity number *g_id*, from a
        list of all couples *couples*.

        :param g_id: generation identifier
        :type g_id: ``int``
        :param couples: list of all constituent couples
        :type couples: ``list`` of ``Couple``
        """
        self.cs = couples
        self.n = len(couples)
        self.id = g_id
        self.preg = self.population_register()
        self.gini = None
        self.x = self.y = None

    def adult_population(self):
        """
        return lists of all men and women within the population

        :return: tuple of lists of all men and of all women
        :rtype: ``tuple`` of ``list`` of ``Person``
        """
        men = []
        women = []
        for couple in self.cs:
            men.append(couple.hb)
            women.append(couple.wf)
        return men, women

    def distribute_children(self):
        """
        distribute children randomly among all families in the generation, in a
        fashion so that they respect the constraints:

        * The next generation has an equal number of boys and girls
        * the next generation is of the exact same size as the current
            generation

        sets the respective number of children within each Couple object
        """
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
        """
        produces a population register, a dictionary that links a person to
        its id number as key.

        :return: ``dict`` of ``int``: <Person>
        """
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
        """
        Turn the children of all families in this generation, into a list of
        new adult persons who have inherited wealth, received a new id number.
        Output is separated between men (bachelors) and women (bachelorettes)

        :param bequest_rule: function by which families bequeath wealth
        :type bequest_rule: ``callable[list, float]``
        :return: lists of new single male and female adults
        :rtype: ``tuple`` of ``list`` of ``Person``
        """
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
        """
        Match the single men in *bachelors* and the single women in
        *bachelorettes*. The matches respects a marital tradition
        *marital_tradition*, which matches a match list based on the statistics
        of the singles.

        This method then "marries" these matched singles into new ``Couple``
        objects, and creates a new generation from all new couples.

        :param bachelors: list of all single men
        :type bachelors: ``list`` of ``Person``
        :param bachelorettes: list of all single women
        :type bachelorettes: ``list`` of ``Person``
        :param marital_tradition: function by which singles match
        :type marital_tradition: ``callable[numpy.Array, numpy.Array]``
        :return: new generation of couples
        :rtype: Generation
        """
        bachelor_stats = _dict_to_statslist(bachelors)
        bachelorette_stats = _dict_to_statslist(bachelorettes)
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
        """
        Make a generation of couples with children, create a new generation of
        adult couples. The current generation bequeaths wealth by a rule
        *bequest_rule*; singles match by a tradition *marital_tradition*.
        :param bequest_rule: function by which families bequeath wealth
        :type bequest_rule: ``callable[list, float]``
        :param marital_tradition: function by which singles match
        :type marital_tradition: ``callable[numpy.Array, numpy.Array]``
        :return: new generation from current generation's children
        :rtype: Generation
        """
        bach_m, bach_f = self.produce_next_gen_bachelors(bequest_rule)
        new_gen = self.match_bachelors(bach_m, bach_f, marital_tradition)
        return new_gen


def _dict_to_statslist(bach_dict):
    m = len(bach_dict.itervalues().next().to_array())
    bachelor_stats = np.zeros((len(bach_dict), m))
    i = 0
    for person in bach_dict.values():
        bachelor_stats[i, :] = person.to_array()
        i = i + 1
    return bachelor_stats
