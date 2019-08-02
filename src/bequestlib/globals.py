import datetime

import numpy as np
from decouple import config

class BequestSettings:
    def __init__(self):
        self.TIMESTAMP = datetime.datetime.now().strftime("%Y%m%d%H%M")
        self.P = [0.35, 0.45, 0.1, 0.06, 0.03, 0.01]
        self.G = np.power(1.02, 25) - 1
        self.N_POPULATION = config('population_size', cast=int)
        self.NU = config('leisure_preference', cast=float)
        self.E_S = 1
        self.GAMMA = config('bequest_preference', cast=float)
        self.BEQUEST_MODULE = config('bequest_module')

    def set_config(self, attribute, value):
        setattr(self, attribute, value)
        self.assert_reproduction_vector_valid()

    def assert_reproduction_vector_valid(self):
        assert sum(self.P) == 1
        assert sum([(i + 1) * p for i, p in enumerate(self.P)]) == 2


settings = BequestSettings()
