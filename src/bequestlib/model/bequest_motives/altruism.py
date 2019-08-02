from bequestlib.model.bequest_motives.optimizer_abc import AbstractUtilityOptimizer
from bequestlib.globals import G, GAMMA, E_S, NU
import numpy as np


class UtilityOptimizer(AbstractUtilityOptimizer):
    def optimize_utility(self, inh_wealth: float,
                         n_children: int,
                         mu_exp: float,
                         tax_rate: float):
        i = inh_wealth
        k = n_children
        perceived_w = (mu_exp * k) / ((1 + G) * (1 - tax_rate))
        e = np.maximum((E_S - NU * (i + perceived_w)) / (1. + NU), 0)
        w = e + i
        c = (1 - GAMMA) * (e + i + perceived_w)
        b = (1 + G) * GAMMA * (e + i + perceived_w) - (1 - GAMMA) / (1 - tax_rate) * mu_exp * k
        if b < 0:
            b = 0
            e = (1 - GAMMA - NU * i) / (1 - GAMMA + NU)
            c = (1 - GAMMA) / NU * (E_S - e)
        return w, e, c, b
