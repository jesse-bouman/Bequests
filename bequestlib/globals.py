import numpy as np
from configparser import ConfigParser
import datetime
import os

TIMESTAMP = datetime.datetime.now().strftime("%Y%m%d%H%M")
curr_path = os.path.abspath(os.path.dirname(__file__))
config_path = os.path.join(curr_path, '..', 'config.ini')


P = [0.35, 0.45, 0.1, 0.06, 0.03, 0.01]
# P = [0.05, 0.9, 0.05]
G = np.power(1.02, 25) - 1

psr = ConfigParser()
psr.read(config_path)

section = 'output_settings'
OUTFOLDER = psr.get(section, 'outfolder')

section = 'Runtime Settings'
N_POPULATION = psr.getint(section, 'population_size')
NU = psr.getfloat(section, 'leisure_preference')
E_S = 1
GAMMA = psr.getfloat(section, 'bequest_preference')


def assert_reproduction_vector_valid(p_vec):
    assert sum(P) == 1
    assert sum([(i + 1) * p for i, p in enumerate(P)]) == 2


assert_reproduction_vector_valid(P)
