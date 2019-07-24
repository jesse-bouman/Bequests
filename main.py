import os

import matplotlib.pyplot as plt

from bequestlib.globals import OUTFOLDER
from bequestlib.metrics.metrics import lorentz_curve
from bequestlib.model.model_closure import run_simulation
from bequestlib.model.society_rules import (all_children_equal, best_partner_is_richest_partner)


def main():
    if not os.path.exists(OUTFOLDER):
        os.mkdir(OUTFOLDER)
    os.chdir(OUTFOLDER)
    for tax_rate in [0.2, 0.4, 0.6, 0.8]:
        result = run_simulation(all_children_equal, best_partner_is_richest_partner, tax_rate)
        gen = result.result_gen
        print(gen.total_labour())
        plt.plot(*lorentz_curve(gen), label=f'{tax_rate*100} %')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()

