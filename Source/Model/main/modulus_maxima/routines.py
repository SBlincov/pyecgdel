"""
Вспомогательные фукнции для поиска экстремумов детализирующих вейвлет-коэффициентов.
"""

from Source.Model.main.modulus_maxima.modulus_maxima import ModulusMaxima
from scipy.signal import argrelextrema
from Source.Model.main.search.closest_position import *
import numpy as np

def get_mms(wdc):
    mins = argrelextrema(wdc, np.less)[0]
    maxs = argrelextrema(wdc, np.greater)[0]
    peaks = np.sort(np.concatenate([mins, maxs]))
    mms = []
    for id in range(0, len(peaks)):
        peak = peaks[id]
        mm = ModulusMaxima(peak, id, wdc)
        mms.append(mm)
    return mms


def get_left_mm(mms, index):
    indexes = [x.index for x in mms]
    id = get_closest(indexes, index)
    if mms[id].index < index:
        return mms[id]
    else:
        return mms[id - 1]


def get_right_mm(mms, index):
    indexes = [x.index for x in mms]
    id = get_closest(indexes, index)
    if mms[id].index > index:
        return mms[id]
    else:
        return mms[id + 1]


def get_lr_mms_in(ecg_lead, scale_id, left, right):
    mms = [mm for mm in ecg_lead.mms[scale_id] if left <= mm.index < right]
    return mms


def get_rl_mms_in(ecg_lead, scale_id, left, right):
    mms = get_lr_mms_in(ecg_lead, scale_id, left, right)
    mms.reverse()
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
