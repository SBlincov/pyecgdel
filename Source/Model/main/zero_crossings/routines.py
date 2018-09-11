"""
Вспомогательные функции, связывающие пересечения нуля и экстремумы детализирующих вейвлет-коэффииентов.
"""

from Source.Model.main.zero_crossings.zero_crossing import *
import numpy as np


def get_zcs(wdc, mms):
    indexes = np.where(np.diff(np.sign(wdc)))[0] + 1

    zcs = []
    r_mms = []
    mm_id = 0
    for id in range(0, len(indexes)):
        index = indexes[id]

        # Define list of left mms
        if id > 0:
            l_mms = r_mms
        else:
            l_mms = []
            while mm_id < len(mms) and mms[mm_id].index < index:
                l_mms.append(mms[mm_id])
                mm_id += 1
        l_mms.reverse()

        # Define list of right mms
        r_index = indexes[id + 1] if id < len(indexes) - 1 else len(wdc) - 1
        r_mms = []
        while mm_id < len(mms) and mms[mm_id].index < r_index:
            r_mms.append(mms[mm_id])
            mm_id += 1

        zc = ZeroCrossing(index, id, l_mms, r_mms)
        zcs.append(zc)

    return zcs


def get_left_zc(zcs, index):
    indexes = [x.index for x in zcs]
    id = get_closest(indexes, index)
    if zcs[id].index < index:
        return zcs[id]
    else:
        return zcs[id - 1]


def get_right_zc(zcs, index):
    indexes = [x.index for x in zcs]
    id = get_closest(indexes, index)
    if zcs[id].index > index:
        return zcs[id]
    else:
        return zcs[id + 1]


def get_zcs_in_window(zcs, begin_index, end_index):
    indexes = [x.index for x in zcs]
    begin_id = get_closest(indexes, begin_index)
    if zcs[id].index < begin_index:
        begin_id += 1
    end_id = get_closest(indexes, end_index)
    if zcs[id].index >= end_index:
        end_id -= 1
    return zcs[begin_id:end_id+1]