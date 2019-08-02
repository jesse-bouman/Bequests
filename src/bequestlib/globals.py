import datetime

import numpy as np
from decouple import config

TIMESTAMP = datetime.datetime.now().strftime("%Y%m%d%H%M")

P = [0.35, 0.45, 0.1, 0.06, 0.03, 0.01]
# P = [0.05, 0.9, 0.05]
G = np.power(1.02, 25) - 1


OUTFOLDER = config('outfolder')

N_POPULATION = config('population_size', cast=int)
NU = config('leisure_preference', cast=float)
E_S = 1
GAMMA = config('bequest_preference', cast=float)
BEQUEST_MODULE = config('bequest_module')


def assert_reproduction_vector_valid(p_vec):
    assert sum(P) == 1
    assert sum([(i + 1) * p for i, p in enumerate(p_vec)]) == 2


assert_reproduction_vector_valid(P)
