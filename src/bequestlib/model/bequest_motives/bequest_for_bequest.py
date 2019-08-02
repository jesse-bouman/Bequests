from bequestlib.model.bequest_motives.optimizer_abc import AbstractUtilityOptimizer
import numpy as np
from bequestlib.globals import settings


class UtilityOptimizer(AbstractUtilityOptimizer):
    def optimize_utility(self, inh_wealth: float,
                         n_children: int,
                         mu_exp: float,
                         tax_rate: float):
        e = np.maximum((1 - settings.NU * inh_wealth) / (1 + settings.NU), 0)
        w = inh_wealth + e
        c = (1 - settings.GAMMA) * w
        b = (1 + settings.G) * settings.GAMMA * w
        return w, e, c, b
