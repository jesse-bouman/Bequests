from bequestlib.model.bequest_motives.optimizer_abc import AbstractUtilityOptimizer
from bequestlib.globals import settings
import numpy as np


class UtilityOptimizer(AbstractUtilityOptimizer):
    def optimize_utility(self, inh_wealth: float,
                         n_children: int,
                         mu_exp: float,
                         tax_rate: float):
        i = inh_wealth
        k = n_children
        g = settings.G
        nu = settings.NU
        gamma = settings.GAMMA

        perceived_w = (mu_exp * k) / (2 * (1 + g) * (1 - tax_rate))
        e = np.maximum((settings.E_S - nu * (i + perceived_w)) / (1. + nu), 0)
        w = e + i
        c = (1 - gamma) * (e + i + perceived_w)
        b = (1 + g) * gamma * (e + i + perceived_w) - (1 + g) * perceived_w
        if b < 0:
            b = 0
            e = (1 - gamma - nu * i) / (1 - gamma + nu)
            w = e + i
            c = (1 - gamma) / nu * (settings.E_S - e)
            if e < 0:
                print('negative e')
                e = 0
                w = inh_wealth
                c = w
        return w, e, c, b
