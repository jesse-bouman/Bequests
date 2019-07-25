from numpy.random import RandomState

SEED = 1

RANDOM_STATE = RandomState(SEED)


def get_random_state():
    global RANDOM_STATE
    return RANDOM_STATE
