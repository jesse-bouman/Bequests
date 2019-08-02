from abc import ABC, abstractmethod
from typing import Tuple


class AbstractUtilityOptimizer(ABC):

    @abstractmethod
    def optimize_utility(self, inh_wealth: float,
                         n_children: int,
                         mu_exp: float,
                         tax_rate: float) -> Tuple[float, float, float, float]:
        pass
