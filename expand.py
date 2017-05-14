import pandas as pd
from itertools import product
from collections import OrderedDict

def expand(data_dict, nesting=None):
    assert isinstance(data_dict, dict)
    data_dict = OrderedDict(data_dict)
    if not nesting:
        rows = product(*data_dict.values())
        final_df = pd.DataFrame.from_records(rows,
                                             columns=data_dict.keys())
        return final_df

    grid_joint = OrderedDict({k: v for k, v in data_dict.items() if k in nesting})
    nest_len = [len(grid_joint[k]) for k in grid_joint.keys()]
    assert len(set(nest_len)) == 1

    lst = [grid_joint[k] for k in grid_joint.keys()]
    nested = list(zip(*lst))
    nesting = sorted(nesting, key=lambda x:list(data_dict.keys()).index(x))
    new_dict = OrderedDict({tuple(nesting): nested})
    grid_remaining = OrderedDict({k: v for k, v in data_dict.items() if
                      not k in nesting})
    grid_combined = OrderedDict({**new_dict, **grid_remaining})

    rows = product(*grid_combined.values())
    final_df = pd.DataFrame.from_records(rows, columns=grid_combined.keys())
    tup_cols = [x for x in final_df.columns if isinstance(x, tuple)][0]
    for i, val in enumerate(tup_cols):
        final_df[val] = [x[i] for x in final_df[tup_cols]]
    final_df = final_df.drop(tup_cols,axis=1)
    final_df = final_df[list(data_dict.keys())]
    return final_df
