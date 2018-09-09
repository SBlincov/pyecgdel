from bisect import bisect_left
import numpy as np


def get_closest(num_list, num):
    pos = np.searchsorted(num_list, num)

    if pos < len(num_list) - 1:
        before = num_list[pos]
        after = num_list[pos + 1]
        if num <= before:
            return pos
        elif num >= after:
            return pos + 1
        else:
            if after - num < num - before:
               return pos
            else:
               return pos + 1
    else:
        return pos

