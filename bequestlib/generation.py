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
        self.creg = None
        self.gini = None
        self.x = self.y = None

    def __getitem__(self, item):
        """
        Getter function that makes a generation dict-like get
        a couple by its couple id

        :param item: couple id
        :type item: int
        :return: couple corresponding to couple id
        :rtype: Couple
        """
        if self.creg is None:
            self.creg = self.couple_register()
        return self.creg[item]

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

    def couple_register(self):
        """
        Creates a couple register: a dictionary of all couple ids to
        their respective couples.

        :return: couple dict
        :rtype: dict of str: <Couple>
        """
        couple_reg = {}
        for couple in self.cs:
            couple_reg[couple.id] = couple
        return couple_reg

    def to_array(self):
        """
        Turn the couple population into a single numpy array of
        important stats. Contains (in this order)

        * 0 : couple id
        * 1 : inherited wealth
        * 2 : total acquired wealth
        * 3 : time spent working

        :return: array of couple stats
        :rtype: numpy.array
        """
        array = np.zeros([self.n, 4])
        i = 0
        for couple in self.cs:
            array[i, :] = couple.to_array()
            i = i + 1
        return array


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

    def redistribute_taxes(self, bachelors, bachelorettes, tax_rate):
        s = tax_rate
        total_tax = 0
        for id, person in bachelors.items():
            tax = s * person.inh
            person.inh-=tax
            total_tax+=tax
        for id, person in bachelorettes.items():
            tax = s * person.inh
            person.inh-=tax
            total_tax+=tax
        lump_sum = total_tax/(len(bachelors)+len(bachelorettes))

        for id, person in bachelors.items():
            person.inh += lump_sum
        for id, person in bachelorettes.items():
            person.inh += lump_sum
        return bachelors, bachelorettes

    def time_spent_working(self):
        c = self.cs
        e = 0
        for couple in c:
            e_i = couple.e
            e+=e_i
        return e


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

    def produce_new_generation(self, bequest_rule, marital_tradition, tax_rate):
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
        bach_m, bach_f = self.redistribute_taxes(bach_m, bach_f, tax_rate)
        new_gen = self.match_bachelors(bach_m, bach_f, marital_tradition)
        return new_gen

    def assign_deciles(self, measure='w'):
        """
        Measure deciles in the population according to measure *measure*,
        and assign them to each constituent couple.

        :param measure: measure to sort couples by. Default is 'w', total wealth
        :type measure: str
        """
        measure_dict = {'inh_w': 1, 'w': 2, 'e': 3}
        column = measure_dict[measure]
        decile_edges = np.zeros(10)

        stats_array = self.to_array()
        for i in range(10):
            decile = np.percentile(stats_array[:, column], 10*(i+1))
            decile_edges[i] = decile
        for couple in self.cs:
            decile = sum(decile_edges < couple.w) + 1
            couple.set_decile(decile)

def _dict_to_statslist(bach_dict):
    """
    Turn the dictionary of bachelor(ette)s into a list of important
    stats.

    :param bach_dict: dict of bachelors: key: id, value: Person
    :type bach_dict: dict of str: <Person>
    :return: list of all bachelor stats
    :rtype: numpy.array
    """
    m = len(next(iter(bach_dict.values())).to_array())
    bachelor_stats = np.zeros((len(bach_dict), m))
    i = 0
    for person in bach_dict.values():
        bachelor_stats[i, :] = person.to_array()
        i = i + 1
    return bachelor_stats
