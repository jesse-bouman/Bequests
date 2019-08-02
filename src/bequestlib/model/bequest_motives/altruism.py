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
        g = settings.g
        nu = settings.NU
        gamma = settings.GAMMA

        perceived_w = (mu_exp * k) / ((1 + g) * (1 - tax_rate))
        e = np.maximum((settings.E_S - nu * (i + perceived_w)) / (1. + nu), 0)
        w = e + i
        c = (1 - gamma) * (e + i + perceived_w)
        b = (1 + g) * gamma * (e + i + perceived_w) - (1 - gamma) / (1 - tax_rate) * mu_exp * k
        if b < 0:
            b = 0
            e = (1 - gamma - nu * i) / (1 - gamma + nu)
            c = (1 - gamma) / nu * (settings.E_S - e)
        return w, e, c, b
