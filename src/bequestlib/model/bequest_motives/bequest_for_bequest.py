from bequestlib.model.bequest_motives.optimizer_abc import AbstractUtilityOptimizer
import numpy as np
from bequestlib.globals import GAMMA, NU, G


class UtilityOptimizer(AbstractUtilityOptimizer):
    def optimize_utility(self, inh_wealth: float,
                         n_children: int,
                         mu_exp: float,
                         tax_rate: float):
        e = np.maximum((1 - NU * inh_wealth) / (1 + NU), 0)
        w = inh_wealth + e
        c = (1 - GAMMA) * w
        b = (1 + G) * GAMMA * w
        return w, e, c, b
