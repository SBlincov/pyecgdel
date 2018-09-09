from bisect import bisect_left
import numpy as np


def get_closest(num_list, num):
    pos = np.searchsorted(num_list, num, side='right')

    if pos > len(num_list) - 1:
        return pos - 1
    else:
        if pos == 0:
            if abs(num_list[pos] - num) < abs(num_list[pos + 1] - num):
                return pos
            else:
                return pos + 1
        elif pos == len(num_list) - 1:
            if abs(num_list[pos] - num) < abs(num_list[pos - 1] - num):
                return pos
            else:
                return pos - 1
        else:
            indexes = [pos - 1, pos, pos + 1]
            cands = [abs(num_list[indexes[0]] - num), abs(num_list[indexes[1]] - num), abs(num_list[indexes[2]] - num)]
            return indexes[np.argmin(cands)]

