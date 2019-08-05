import matplotlib.pyplot as plt

from analyses.helpers import OutputData
from bequestlib.globals import settings
from bequestlib.metrics.metrics import gini, total_wealth
from bequestlib.model.model_closure import run_simulation, SimulationResult
from bequestlib.model.society_rules import (all_children_equal, love_is_blind)
from bequestlib.random import set_random_state_with_seed

set_random_state_with_seed(473150973)

# Settings for full reproduceability:
"""
[settings]
bequest_module: bequest_for_bequest
n_couples: 1000
leisure_preference = 0.3
bequest_preference = 0.4
interest_earnings = 0.64060599446
i0_inheritance = 0
i0_n_couples_with_inheritance = %(n_couples)s
"""

settings.set_config('N_POPULATION', 10000)

setups = [(0, 5000), (10000, 1), (100, 1000)]
final_gens = list()
for setup in setups:
    inh_0, rich_couples = setup
    output = OutputData(f'{inh_0}_{rich_couples}')

    settings.set_config('I0_INHERITANCE', inh_0)
    settings.set_config('I0_COUPLES_WITH_INHERITANCE', rich_couples)
    test_result: SimulationResult = run_simulation(all_children_equal,
                                                   love_is_blind,
                                                   0.0)
    print(len(test_result.generations))

    x = [i for i, _ in enumerate(test_result._results)]
    y = [total_wealth(gen) for gen in test_result.generations]
    ginis = [gini(gen) for gen in test_result.generations]
    success = [int(r['success']) for r in test_result._results]

    output.add_data([x], 'Period')
    output.add_data([y], 'Total_Wealth')
    output.add_data([ginis], 'Gini_Coefficient')
    output.add_data([success], 'Success_Flag')
    output.write_data()

    plt.plot(x, ginis)

    final_gens.append(test_result.result_gen)

for gen in final_gens[1:]:
    print(gen.significance_of_difference_to_other_gen(final_gens[0]))

plt.show()