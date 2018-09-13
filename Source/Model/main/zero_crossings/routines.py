"""
Вспомогательные функции, связывающие пересечения нуля и экстремумы детализирующих вейвлет-коэффииентов.
"""

from Source.Model.main.zero_crossings.zero_crossing import *
import numpy as np
import copy


def get_zcs(wdc, mms):
    indexes = np.where(np.diff(np.sign(wdc)))[0] + 1

    zcs = []
    r_mms = []
    mm_id = 0
    for id in range(0, len(indexes)):
        index = indexes[id]

        # Define list of left mms
        if id > 0:
            l_mms = copy.deepcopy(r_mms)
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


def get_zcs_in_window(wdc, zcs, begin_index, end_index):
    indexes = [x.index for x in zcs]

    begin_index_for_zc = begin_index + 1
    end_index_for_zc = end_index - 1

    begin_index_for_mm = begin_index
    end_index_for_mm = end_index - 1

    begin_id = get_closest(indexes, begin_index_for_zc)
    if zcs[begin_id].index < begin_index_for_zc:
        begin_id += 1
    end_id = get_closest(indexes, end_index_for_zc)
    if zcs[end_id].index >= end_index_for_zc:
        end_id -= 1

    target_zcs = copy.deepcopy(zcs[begin_id: end_id + 1])

    if len(target_zcs) > 0:

        left_zc = target_zcs[0]
        if len(left_zc.l_mms) > 0:
            num_passed = 0
            while num_passed < len(left_zc.l_mms) and left_zc.l_mms[num_passed].index >= begin_index_for_mm:
                num_passed += 1
            if num_passed > 0:
                tmp_mms = left_zc.l_mms[0:num_passed]
                if len(left_zc.l_mms) > num_passed:
                    tmp_mm = ModulusMaxima(begin_index_for_mm, left_zc.l_mms[num_passed].id, wdc)
                    tmp_mms.append(tmp_mm)
                left_zc.l_mms = tmp_mms
                left_zc.zc_proc()
            else:
                first_mm = ModulusMaxima(begin_index_for_mm, left_zc.l_mms[0].id, wdc)
                left_zc.l_mms = [first_mm]
                left_zc.zc_proc()

        right_zc = target_zcs[-1]
        if len(right_zc.r_mms) > 0:
            num_passed = 0
            while num_passed < len(right_zc.r_mms) and right_zc.r_mms[num_passed].index <= end_index_for_mm:
                num_passed += 1
            if num_passed > 0:
                tmp_mms = right_zc.r_mms[0:num_passed]
                if len(right_zc.r_mms) > num_passed:
                    tmp_mm = ModulusMaxima(end_index_for_mm, right_zc.r_mms[num_passed].id, wdc)
                    tmp_mms.append(tmp_mm)
                right_zc.r_mms = tmp_mms
                right_zc.zc_proc()
            else:
                last_mm = ModulusMaxima(end_index_for_mm, right_zc.r_mms[-1].id, wdc)
                right_zc.r_mms = [last_mm]
                right_zc.zc_proc()

    return target_zcs