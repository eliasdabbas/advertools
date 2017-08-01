from collections import OrderedDict
from itertools import product

import pandas as pd


def expand_plain(data_dict):
    """
    Generate all possible combinations of values of a dictionary.

    :param data_dict: a dictionary
    :return: a data frame where each row represents a combination,
    and column names are the dictionary keys

    >>> data_dict = {
    ... 'letters': ['a', 'b', 'c'],
    ... 'nums': [1, 2],
    ... 'days': ['mon', 'tues']
    ... }
    >>> expand_plain(data_dict)
       letters  nums  days
    0        a     1   mon
    1        a     1  tues
    2        a     2   mon
    3        a     2  tues
    4        b     1   mon
    5        b     1  tues
    6        b     2   mon
    7        b     2  tues
    8        c     1   mon
    9        c     1  tues
    10       c     2   mon
    11       c     2  tues
    """
    rows = product(*data_dict.values())
    final_df = pd.DataFrame.from_records(rows,
                                         columns=data_dict.keys())
    return final_df


def dict_split(d, lst):
    """
    Split a dictionary in two OrderedDicts, one with items present in `lst`,
    and another with items that are not.
    :rtype: collections.OrderedDict
    :param d: a dictionary
    :param lst: a list of keys to filter by
    :return: two OrderedDict's one with and one without the keys in `lst`

    >>> d = {
    ... 'a': [1, 2, 3],
    ... 'b': [4, 5, 6],
    ... 'c': [7, 8, 9],
    ... 'd': [4, 5, 6],
    ... }
    >>> dict_split(d, ['a', 'b'])
    (OrderedDict([('a', [1, 2, 3]), ('b', [4, 5, 6])]), OrderedDict([('c', [7, 8, 9]), 'd', [4,5,6]]))

    """
    d = OrderedDict(d)
    d_include = OrderedDict({k: v for k, v in d.items() if k in lst})
    d_exclude = OrderedDict({k: v for k, v in d.items() if not k in lst})
    return d_include, d_exclude



def expand(data_dict, nesting=None):
    """
    Return a DataFrame where column names are data_dict's keys and each
    row is a combination of the data_dict values.

    This is a wrapper around `itertools.product` with one important
    addition; making sure that the rows of two or more keys remain
    together as a unit.

    Assume you want to generate all possible keywords from a list of
    car makes and models, together with a list of possible purchase intent
    words.

    >>> data_dict = {
    ...        'make': ['toyota', 'toyota', 'ford', 'ford'],
    ...        'model': ['yaris', 'camry', 'mustang', 'focus'],
    ...        'buy': ['buy', 'best', 'price']
    ...        }
    >>> expand(data_dict=data_dict, nesting=['make', 'model'])
          make    model    buy
    0   toyota    yaris    buy
    1   toyota    yaris   best
    2   toyota    yaris  price
    3   toyota    camry    buy
    4   toyota    camry   best
    5   toyota    camry  price
    6     ford  mustang    buy
    7     ford  mustang   best
    8     ford  mustang  price
    9     ford    focus    buy
    10    ford    focus   best
    11    ford    focus  price

    Without the `nesting` argument, we would have ended up with
    "toyota mustang" and "ford camry" as possible combinations.
    """
    assert isinstance(data_dict, dict)
    data_dict = OrderedDict(data_dict)
    if not nesting:
        return expand_plain(data_dict)

    grid_joint = OrderedDict({k: v for k, v in data_dict.items() if k in nesting})
    nest_len = [len(grid_joint[k]) for k in grid_joint.keys()]
    assert len(set(nest_len)) == 1, ('Make sure nested lists have the same length')

    lst = [grid_joint[k] for k in grid_joint.keys()]
    nested = list(zip(*lst))
    nesting = sorted(nesting, key=lambda x:list(data_dict.keys()).index(x))
    new_dict = OrderedDict({tuple(nesting): nested})
    grid_remaining = OrderedDict({k: v for k, v in data_dict.items() if
                      not k in nesting})
    grid_combined = OrderedDict({**new_dict, **grid_remaining})

    # rows = product(*grid_combined.values())
    # final_df = pd.DataFrame.from_records(rows, columns=grid_combined.keys())
    final_df = expand_plain(grid_combined)
    tup_cols = [x for x in final_df.columns if isinstance(x, tuple)][0]
    for i, val in enumerate(tup_cols):
        final_df[val] = [x[i] for x in final_df[tup_cols]]
    final_df = final_df.drop(tup_cols,axis=1)
    final_df = final_df[list(data_dict.keys())]
    return final_df

# dikt = {
#     'letters': list('abcd'),
#     'nums': [1,2,3,4],
#     'days': ['sun', 'mon', 'tue']
# }
#
# dict_split(dikt, ['letters', 'nums'])


