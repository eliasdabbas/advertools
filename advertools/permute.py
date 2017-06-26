import pandas as pd
from itertools import permutations

def permute(keys, keys_to_keep=None, min_len=2, max_len=3):
    final = []
    counter = 0
    if keys_to_keep is None:
        for i in range(min_len, max_len + 1):
            for j in permutations(keys, i):
                final.append(list(j))
                print('{:>3}'.format(counter), list(j))
                counter += 1
        return final

    for i in range(min_len, max_len + 1):
            for j in permutations(keys,i):
                if any([key in keys_to_keep for key in j]):
                    final.append(list(j))
                    print('{:>3}'.format(counter), list(j))
                    counter += 1
    return final
