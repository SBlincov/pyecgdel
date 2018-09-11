"""
Вспомогательные фукнции для поиска экстремумов детализирующих вейвлет-коэффициентов.

Входные параметры:
    start_index - индекс начала поиска.
    wdc - детализирующие вейвлет-коэффициенты.
"""

from Source.Model.main.params.common import *
from Source.Model.main.modulus_maxima.modulus_maxima import ModulusMaxima


def find_left_mm(start_index, wdc):

    if start_index <= 0:
        return ModulusMaxima(0, wdc)

    center_id = start_index
    prev_id = start_index - 1
    next_id = start_index + 1

    while prev_id >= 0:

        next_diff = wdc[center_id] - wdc[next_id]
        prev_diff = wdc[prev_id] - wdc[center_id]

        if next_diff * prev_diff < 0:
            break
        elif abs(prev_diff) < EPSILON:
            constant_period = 0
            while prev_id >= 0 and abs(prev_diff) < EPSILON:
                constant_period += 1
                prev_id -= 1
                if prev_id >= 0:
                    prev_diff = wdc[prev_id] - wdc[center_id]
                else:
                    prev_diff = wdc[0] - wdc[center_id]
            center_id = prev_id + 1
        else:
            prev_id -= 1
            center_id -= 1
            next_id -= 1

    mm = ModulusMaxima(center_id, wdc)

    return mm


def find_right_mm(start_index, wdc):

    if start_index >= len(wdc) - 1:
        return ModulusMaxima(len(wdc) - 1, wdc)

    center_id = start_index
    prev_id = start_index - 1
    next_id = start_index + 1

    while next_id <= len(wdc) - 1:

        next_diff = wdc[next_id] - wdc[center_id]
        prev_diff = wdc[center_id] - wdc[prev_id]

        if next_diff * prev_diff < 0:
            break
        elif abs(next_diff) < EPSILON:
            constant_period = 0
            while next_id <= len(wdc) - 1 and abs(next_diff) < EPSILON:
                constant_period += 1
                next_id += 1
                if next_id <= len(wdc) - 1:
                    next_diff = wdc[next_id] - wdc[center_id]
                else:
                    next_diff = wdc[len(wdc) - 1] - wdc[center_id]
            center_id = next_id - 1
        else:
            prev_id += 1
            center_id += 1
            next_id += 1

    mm = ModulusMaxima(center_id, wdc)

    return mm


def get_lr_mms_in(left, right, wdc):
    mms = []

    mm_curr = find_right_mm(left, wdc)
    mm_next = mm_curr

    while mm_next.index < right:
        mm_curr = mm_next
        mms.append(mm_curr)
        mm_next = find_right_mm(mm_curr.index + 1, wdc)

    return mms


def get_rl_mms_in(right, left, wdc):
    mms = []

    mm_curr = find_left_mm(right, wdc)
    mm_next = mm_curr

    while mm_next.index > left:
        mm_curr = mm_next
        mms.append(mm_curr)
        mm_next = find_left_mm(mm_curr.index - 1, wdc)

    return mms


def get_correct_mms_ids(mms):
    correct_mms_ids = []

    for mm_id in range(0, len(mms)):
        if mms[mm_id].correctness:
            correct_mms_ids.append(mm_id)

    return correct_mms_ids


def get_incorrect_mms_ids(mms):
    incorrect_mms_ids = []

    for mm_id in range(0, len(mms)):
        if not mms[mm_id].correctness:
            incorrect_mms_ids.append(mm_id)

    return incorrect_mms_ids

