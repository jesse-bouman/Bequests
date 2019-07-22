from bequestlib.random import get_random_state
from numpy.random import RandomState


def all_children_equal(children, b):
    """
    Bequest rule. Bequeathes an equal part of all planned bequests
    to each child.

    :param children: list of children. ``True`` for boy, ``False`` for a girl
    :type children: ``list`` of ``bool``
    :param b: total amount of planned bequests
    :type b: float
    :return: list of bequests to each respective child
    :rtype: ``list`` of ``float``
    """
    return [b/len(children)]*len(children)


def oldest_gets_all(children, b):
    """
    Bequest rule. Gives all planned bequest money to the eldest

    :param children: list of children. ``True`` for boy,
        ``False`` for a girl
    :type children: ``list`` of ``bool``
    :param b: total amount of planned bequests
    :type b: float
    :return: list of bequests to each respective child
    :rtype: ``list`` of ``float``
    """
    return [b] + [0.]*(len(children)-1)


def male_primogeniture(children, b):
    """
    Bequest rule. Give all planned bequest money to eldest son. If
    no sons, the eldest daughter receives all

    :param children: list of children. ``True`` for boy,
        ``False`` for a girl
    :type children: ``list`` of ``bool``
    :param b: total amount of planned bequests
    :type b: float
    :return: list of bequests to each respective child
    :rtype: ``list`` of ``float``
    """
    beq_vec = [0.]*len(children)
    # if there are men among the children:
    if sum(children) != 0:
        first_found = False
        for i, child in enumerate(children):
            if child and not first_found:
                # bequest all to eldest son
                beq_vec[i] = b
                first_found = True
    # if there are no men among the children:
    else:
        # eldest daughter gets all
        beq_vec[0] = b
    return beq_vec


def best_partner_is_richest_partner(bachelor_stats, bachelorette_stats):
    """
    Marital rule. Matches bachelors according to their wealth. Bachelors
    are coupled by sorting the respective lists by inherited wealth.

    :param bachelor_stats: list of bachelor stats. Contains ids and inherited
        wealth
    :type bachelorette_stats: numpy.array
    :param bachelorette_stats: list of bachelorette stats. Contains ids and
        inherited wealth
    :type bachelorette_stats: numpy.array
    :return: lists of ids that describe the matches
    """
    order_bach = bachelor_stats[:, -1].argsort()
    order_bachts = bachelorette_stats[:, -1].argsort()
    groom_order = bachelor_stats[order_bach][:, 0]
    bride_order = bachelorette_stats[order_bachts][:, 0]
    return groom_order.astype(int), bride_order.astype(int)


def love_is_blind(bachelor_stats, bachelorette_stats):
    """
    Marital rule. Matches bachelors by chance.

    :param bachelor_stats: list of bachelor stats. Contains ids and inherited
        wealth
    :type bachelorette_stats: numpy.array
    :param bachelorette_stats: list of bachelorette stats. Contains ids and
        inherited wealth
    :type bachelorette_stats: numpy.array
    :return: lists of ids that describe the matches
    """
    b_ids = bachelor_stats[:, 0]
    random: RandomState = get_random_state()
    random.shuffle(b_ids)
    groom_order = b_ids
    bride_order = bachelorette_stats[:, 0]
    return groom_order.astype(int), bride_order.astype(int)
