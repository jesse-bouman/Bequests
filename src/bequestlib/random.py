from numpy.random import RandomState
from numpy.random import randint
SEED = randint(1, 10000000)
print(SEED)
RANDOM_STATE = RandomState(SEED)


def get_random_state():
    global RANDOM_STATE
    return RANDOM_STATE
