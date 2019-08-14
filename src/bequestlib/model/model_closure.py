from bequestlib.globals import settings
from bequestlib.model.person import Person
from bequestlib.model.couple import Couple
from bequestlib.model.generation import Generation
import numpy as np
from scipy.stats import ks_2samp
from typing import Callable, Tuple


N_EQUAL_FOR_SUCCESS = 5


def run_simulation(bequest_rule: Callable, marital_rule: Callable, tax_rate):
        result = SimulationResult()
        generator = next_gen_generator(bequest_rule, marital_rule, tax_rate)
        for generation, d, p, success in generator:
            result.add_generation(generation, d, p, success)
            #print(generation.lump_sum)
        return result


class SimulationResult:
    def __init__(self):
        self._results = list()

    @property
    def generations(self):
        return [result['generation'] for result in self._results]

    def add_generation(self, gen: Generation, d_ks: float, p_ks: float, success: bool):
        self._results.append({'generation': gen,
                              'd': d_ks,
                              'p': p_ks,
                              'success': success})

    def run_converged(self) -> bool:
        start_point = -1 * N_EQUAL_FOR_SUCCESS
        return all([r['success'] for r in self._results[start_point:-1]])

    @property
    def result_gen(self) -> Generation:
        if self.generations:
            return self.generations[-1]
        else:
            raise ValueError('No generations simulated yet')


def create_init_couple(inheritance, index):
    couples = int(settings.N_POPULATION / 2.)
    hb = Person(gender=True, parent_couple_id=index)
    wf = Person(gender=False, parent_couple_id=couples - index)
    hb.set_id(index)
    wf.set_id(couples + index)
    wf.add_inheritance(inheritance)
    hb.add_inheritance(0.)
    cp = Couple(husband=hb, wife=wf, c_id=index)
    return cp


def init_generation():
    # set up a fully egalitarian starting generation
    n = settings.N_POPULATION
    couples = int(n / 2.)
    breakp = settings.I0_COUPLES_WITH_INHERITANCE
    rich = [create_init_couple(settings.I0_INHERITANCE, i) for i in range(breakp)]
    poor = [create_init_couple(0, i) for i in range(breakp, couples)]
    couples_list = rich + poor
    gen_1 = Generation(g_id=1, couples=couples_list)
    gen_1.distribute_children()
    for cp in gen_1.cs:
        cp.optimize_utility(0, 0)
    gen_1.lump_sum = 0
    return gen_1


def next_gen_generator(bequest_rule, marital_tradition, tax_rate) -> Tuple[Generation, float,
                                                                           float, bool]:
    adult_gen = init_generation()
    yield adult_gen, None, None, False

    wealths = np.sort(adult_gen.to_array()[:, 1])
    a = wealths / sum(wealths)
    test_period = 0
    tot_period = 0
    while test_period < N_EQUAL_FOR_SUCCESS and tot_period < 200:
        next_gen = adult_gen.produce_new_generation(bequest_rule=bequest_rule,
                                                    marital_tradition=marital_tradition,
                                                    tax_rate=tax_rate)
        d, p = next_gen.significance_of_difference_to_other_gen(adult_gen)
        adult_gen = next_gen
        success = p > 0.5
        if success:
            test_period = test_period + 1
        else:
            test_period = 0
        tot_period = tot_period + 1
        yield adult_gen, d, p, success
