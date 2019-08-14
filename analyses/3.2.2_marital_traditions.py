import matplotlib.pyplot as plt

from analyses.helpers import OutputData
from bequestlib.globals import settings
from bequestlib.metrics.metrics import gini, lorentz_curve
from bequestlib.model.model_closure import run_simulation, SimulationResult
from bequestlib.model.society_rules import (all_children_equal, best_partner_is_richest_partner)
from bequestlib.random import set_random_state_with_seed
import numpy as np

setups = {f'3kmax_b_{i}': [i/100.0, (100 - 2*i)/100, i/100] for i in range(0, 55, 5)}

output_lorentz_curves = OutputData('lorentz_curves')

final_gens = list()
p1s = list()
stds = list()
ginis = list()
i = 0
for name, setup in setups.items():
    print(setup)
    b = setup[0]

    settings.set_config('P', setup)
    test_result: SimulationResult = run_simulation(all_children_equal,
                                                   best_partner_is_richest_partner,
                                                   0.0)
    result_gen = test_result.result_gen
    x, y = lorentz_curve(result_gen)
    if i == 0:
        y0 = y
    if i % 2 == 0:
        plt.plot(x, y0 -y)
    i += 1
    output_lorentz_curves.add_data([x, y], name)
    print(len(test_result.generations))

    p1s.append(b)
    stds.append(np.sqrt(2*b))
    ginis.append(gini(result_gen))

plt.show()
plt.clf()
output_gini = OutputData('gini_vs_stdv_class_society')
output_gini.add_data([p1s, stds, ginis], 'x')
plt.plot(stds, ginis)
plt.show()

output_gini.write_data()
output_lorentz_curves.write_data()