from numpy.random import RandomState

RANDOM_STATE = None


def get_random_state() -> RandomState:
    global RANDOM_STATE
    if not RANDOM_STATE:
        RANDOM_STATE = RandomState()
    return RANDOM_STATE


def set_random_state_with_seed(seed: int):
    global RANDOM_STATE
    RANDOM_STATE = RandomState(seed)


def get_random_state_seed():
    state = get_random_state()
    return state.seed()
