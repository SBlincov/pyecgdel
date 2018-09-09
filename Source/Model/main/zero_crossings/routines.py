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


def get_zcs_in_window(ecg_lead, scale_id, begin_index, end_index):
    zcs = [zc for zc in ecg_lead.zcs[scale_id] if begin_index <= zc.index < end_index]
    return zcs