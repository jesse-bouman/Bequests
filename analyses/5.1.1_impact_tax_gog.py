import matplotlib.pyplot as plt

from analyses.helpers import OutputData
from bequestlib.globals import settings
from bequestlib.metrics.metrics import gini, lorentz_curve
from bequestlib.model.model_closure import run_simulation, SimulationResult
from bequestlib.model.society_rules import (all_children_equal, best_partner_is_richest_partner)
from bequestlib.random import set_random_state_with_seed
import numpy as np

setups_g = {f'g_{i}': i/100 for i in list(range(0, 110, 10))}

output_lorentz_curves = OutputData('lorentz_curves')

final_gens = list()
p1s = list()
ginis = list()
lump_sums = list()
total_bequests = list()
total_wealth = list()
total_inheritance = list()
total_labour = list()
i = 0
for name, setup in setups_g.items():
    print(setup)
    gamma = setup
    settings.set_config('I0_INHERITANCE', 0)
    test_result: SimulationResult = run_simulation(all_children_equal,
                                                   best_partner_is_richest_partner,
                                                   setup)
    result_gen = test_result.result_gen
    x, y = lorentz_curve(result_gen)
    if i == 0:
        y0 = y
    if i % 2 == 0:
        plt.plot(x, y0 -y)
    i += 1
    output_lorentz_curves.add_data([x, y], name)
    print(len(test_result.generations))
    print(result_gen.number_of_idle_people())
    p1s.append(gamma)
    ginis.append(gini(result_gen))
    total_bequests.append(sum([c.b for c in result_gen.cs]))
    total_wealth.append(sum([c.w for c in result_gen.cs]))
    total_inheritance.append(sum([c.inh_wealth for c in result_gen.cs]))
    total_labour.append(sum([c.e for c in result_gen.cs]))
    lump_sums.append(result_gen.lump_sum)

plt.show()
plt.clf()
output_gini = OutputData('tau_analysis')
output_gini.add_data([p1s, ginis, lump_sums, total_bequests, total_labour], 'x')
plt.plot(p1s, total_bequests)
plt.plot(p1s, total_wealth)
plt.plot(p1s, total_inheritance)
plt.show()
output_gini.write_data()
output_lorentz_curves.write_data()