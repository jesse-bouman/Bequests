import datetime

import numpy as np
from decouple import config


class BequestSettings:
    def __init__(self):
        self.TIMESTAMP = datetime.datetime.now().strftime("%Y%m%d%H%M")
        self.P = [0.35, 0.45, 0.1, 0.06, 0.03, 0.01]
        self.G = np.power(1.02, 25) - 1
        self.N_POPULATION = config('n_couples', cast=int) * 2
        self.NU = config('leisure_preference', cast=float)
        self.E_S = 1
        self.GAMMA = config('bequest_preference', cast=float)
        self.BEQUEST_MODULE = config('bequest_module')
        self.I0_INHERITANCE = config('i0_inheritance', cast=float)
        self.I0_COUPLES_WITH_INHERITANCE = config('i0_n_couples_with_inheritance', cast=int)

    def set_config(self, attribute, value):
        setattr(self, attribute, value)
        self.assert_reproduction_vector_valid()

    def assert_reproduction_vector_valid(self):
        chances = sum(self.P)
        if not np.abs(chances - 1) < 1e-10:
            raise ValueError(f"Probabilities for {self.P} do not add up to 1")
        expected_children = sum([(i + 1) * p for i, p in enumerate(self.P)])
        if not np.abs(expected_children - 2) < 1e-10:
            raise ValueError(f'Children vector {self.P} has average {expected_children}, must be 2')


settings = BequestSettings()
