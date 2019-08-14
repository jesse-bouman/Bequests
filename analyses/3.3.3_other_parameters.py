import matplotlib.pyplot as plt

from analyses.helpers import OutputData
from bequestlib.globals import settings
from bequestlib.metrics.metrics import gini, lorentz_curve
from bequestlib.model.model_closure import run_simulation, SimulationResult
from bequestlib.model.society_rules import (all_children_equal, love_is_blind)
from bequestlib.random import set_random_state_with_seed
import numpy as np

setups_g = {f'g_{i}': i/100 for i in range(0, 170, 10)}

output_lorentz_curves = OutputData('lorentz_curves')

final_gens = list()
p1s = list()
ginis = list()
idle = list()
i = 0
for name, setup in setups_g.items():
    print(setup)
    gamma = setup

    settings.set_config('G', setup)
    test_result: SimulationResult = run_simulation(all_children_equal,
                                                   love_is_blind,
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
    print(result_gen.number_of_idle_people())
    if test_result.run_converged():
        idle.append(result_gen.number_of_idle_people()/ result_gen.n)
        p1s.append(gamma)
        ginis.append(gini(result_gen))


plt.show()
plt.clf()
output_gini = OutputData('gamma_analysis')
output_gini.add_data([p1s, ginis], 'x')
plt.plot(p1s, ginis)
plt.plot(p1s, idle)
plt.show()
output_gini.write_data()
output_lorentz_curves.write_data()