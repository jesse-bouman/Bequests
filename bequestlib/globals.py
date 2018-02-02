import numpy as np
from ConfigParser import ConfigParser
import datetime
import os

TIMESTAMP = datetime.datetime.now().strftime("%Y%m%d%H%M")
curr_path = os.path.abspath(os.path.dirname(__file__))
config_path = os.path.join(curr_path, '..', 'config.ini')

NU = 0.3
E_S = 1
GAMMA = 0.4
P = [0.35, 0.45, 0.1, 0.06, 0.03, 0.01]
G = np.power(1.02, 25) - 1

psr = ConfigParser()
psr.read(config_path)

section = 'output_settings'
OUTFOLDER = psr.get(section, 'outfolder')