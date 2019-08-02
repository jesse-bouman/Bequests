import matplotlib.pyplot as plt
import numpy as np

from bequestlib.model.model_closure import run_simulation
from bequestlib.model.society_rules import (all_children_equal, best_partner_is_richest_partner)


def main():
    x = list()
    y = list()
    keeper = list()
    for tax_rate in list(np.arange(0, 0.85, 0.05)) + list(np.arange(0.85, 0.99, 0.01)):
        print(tax_rate)
        result = run_simulation(all_children_equal, best_partner_is_richest_partner, tax_rate)
        gen = result.result_gen
        gen.produce_new_generation(all_children_equal, best_partner_is_richest_partner, tax_rate)
        x.append(tax_rate)
        y.append(gen.lump_sum)
        keeper.append(result.generations[-3:-1])
    plt.plot(x, y)
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()

