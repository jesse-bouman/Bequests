import numpy as np


def all_children_equal(children, b):
    return [b/len(children)]*len(children)


def oldest_gets_all(children, b):
    return [b] + [0.]*(len(children)-1)


def best_partner_is_richest_partner(bachelor_stats, bachelorette_stats):
    order_bach = bachelor_stats[:, -1].argsort()
    order_bachts = bachelorette_stats[:, -1].argsort()
    groom_order = bachelor_stats[order_bach][:,0]
    bride_order = bachelorette_stats[order_bachts][:, 0]
    return groom_order.astype(int), bride_order.astype(int)


def love_is_blind(bachelor_stats, bachelorette_stats):
    b_ids = bachelor_stats[:, 0]
    np.random.shuffle(b_ids)
    groom_order = b_ids
    bride_order = bachelorette_stats[:, 0]
    return groom_order.astype(int), bride_order.astype(int)