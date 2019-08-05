from numpy.random import RandomState
from numpy.random import randint

SEED = None
RANDOM_STATE = None


def get_random_state() -> RandomState:
    global RANDOM_STATE
    if not RANDOM_STATE:

        seed = randint(low=0, high=2**31 - 1)
        RANDOM_STATE = RandomState(seed)
        global SEED
        SEED = seed
    return RANDOM_STATE


def set_random_state_with_seed(seed: int):
    global RANDOM_STATE
    RANDOM_STATE = RandomState(seed)
    global SEED
    SEED = seed


def get_random_state_seed():
    get_random_state()
    global SEED
    return SEED
