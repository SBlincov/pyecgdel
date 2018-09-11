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
            left = abs(num_list[pos - 1] - num)
            center = abs(num_list[pos] - num)
            right = abs(num_list[pos + 1] - num)

            if left <= min(center, right):
                return pos - 1
            if center <= min(left, right):
                return pos
            if right <= min(left, center):
                return pos + 1
