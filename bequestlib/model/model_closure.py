from bequestlib.globals import N_POPULATION
from bequestlib.model.person import Person
from bequestlib.model.couple import Couple
from bequestlib.model.generation import Generation
import numpy as np
from scipy.stats import ks_2samp
from typing import Callable


def run_simulation(bequest_rule: Callable, marital_rule: Callable, tax_rate):
        result = SimulationResult()
        generator = next_gen_generator(bequest_rule, marital_rule, tax_rate)
        for generation, d, p in generator:
            result.add_generation(generation)
        return result


class SimulationResult:
    def __init__(self):
        self.generations = list()

    def add_generation(self, gen: Generation):
        self.generations.append(gen)

    @property
    def result_gen(self) -> Generation:
        if self.generations:
            return self.generations[-1]
        else:
            raise ValueError('No generations simulated yet')


def create_init_couple(inheritance, index):
    couples = int(N_POPULATION / 2.)
    hb = Person(gender=True, parent_couple_id=index)
    wf = Person(gender=False, parent_couple_id=couples - index)
    hb.set_id(index)
    wf.set_id(couples + index)
    hb.add_inheritance(inheritance)
    wf.add_inheritance(0.)
    cp = Couple(husband=hb, wife=wf, c_id=index)
    return cp


def init_generation():
    # set up a fully egalitarian starting generation
    n = N_POPULATION
    couples = int(n / 2.)
    couples_list = [create_init_couple(0.01, i) for i in range(couples)]
    gen_1 = Generation(g_id=1, couples=couples_list)
    gen_1.distribute_children()
    for cp in gen_1.cs:
        cp.optimize_utility(0, 0.0)
    return gen_1


def next_gen_generator(bequest_rule, marital_tradition, tax_rate):
    adult_gen = init_generation()
    wealths = np.sort(adult_gen.to_array()[:, 1])
    a = wealths / sum(wealths)
    test_period = 0
    tot_period = 0
    while test_period < 30 and tot_period < 10:
        next_gen = adult_gen.produce_new_generation(bequest_rule=bequest_rule,
                                                    marital_tradition=marital_tradition,
                                                    tax_rate=tax_rate)
        adult_gen = next_gen

        wealth = np.sort(adult_gen.to_array()[:, 1])
        prev_a = a
        a = wealth / sum(wealth)
        d, p = ks_2samp(prev_a, a)
        if p > 0.5:
            test_period = test_period + 1
        else:
            test_period = 0
        tot_period = tot_period + 1
        yield adult_gen, d, p
