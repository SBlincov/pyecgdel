"""
Класс пересечений нуля детализирующими вейвлет-коэффициентами.
"""

import numpy as np
from ..modulus_maxima.routines import *
from enum import Enum


class InvalidZeroCrossingData(Exception):
    pass


class ExtremumSign(Enum):
    negative = -1
    positive = 1
    unknown = 0

    def __int__(self):
        return self.value


class ZeroCrossing:
    def __init__(self, index, id, l_mms, r_mms):
        self.index = index
        self.id = id

        self.l_mms = l_mms
        self.r_mms = r_mms

        # Global mms
        self.g_l_mm = None
        self.g_r_mm = None
        self.g_ampl = 0.0

        # Local mms
        self.l_l_mm = None
        self.l_r_mm = None
        self.l_ampl = 0.0

        # Special mms
        self.s_l_mm = None
        self.s_r_mm = None
        self.s_ampl = 0.0

        self.extremum_sign = ExtremumSign.unknown

        self.zc_proc()

    def zc_proc(self):
        self.g_l_mm = self.l_mms[np.argmax([abs(mm.value) for mm in self.l_mms])] if len(self.l_mms) > 0 else None
        self.g_r_mm = self.r_mms[np.argmax([abs(mm.value) for mm in self.r_mms])] if len(self.r_mms) > 0 else None
        if self.g_l_mm is not None and self.g_r_mm is not None:
            self.g_ampl = abs(self.g_l_mm.value) + abs(self.g_r_mm.value)

            if self.g_l_mm.value < 0 and self.g_r_mm.value > 0:
                self.extremum_sign = ExtremumSign.positive
            else:
                self.extremum_sign = ExtremumSign.negative

        self.l_l_mm = self.l_mms[0] if len(self.l_mms) > 0 else None
        self.l_r_mm = self.r_mms[0] if len(self.r_mms) > 0 else None
        if self.l_l_mm is not None and self.l_r_mm is not None:
            self.l_ampl = abs(self.l_l_mm.value) + abs(self.l_r_mm.value)



    def special(self, wdc, left_index, right_index):

        right_index -= 1

        l_mms = [mm for mm in self.l_mms if mm.index > left_index]
        if len(l_mms) > 0:
            self.s_l_mm = l_mms[np.argmax([abs(mm.value) for mm in l_mms])]
        else:
            self.s_l_mm = None
        if self.s_l_mm is None:
            if self.index == left_index:
                self.s_l_mm = ModulusMaxima(left_index, self.l_mms[0].id, wdc)
            else:
                left_mm_index = left_index + np.argmax(np.abs(wdc[left_index:self.index]))
                self.s_l_mm = ModulusMaxima(left_mm_index, self.l_mms[0].id, wdc)

        r_mms = [mm for mm in self.r_mms if mm.index < right_index]
        if len(r_mms) > 0:
            self.s_r_mm = r_mms[np.argmax([abs(mm.value) for mm in r_mms])]
        else:
            self.s_r_mm = None
        if self.s_r_mm is None:
            if self.index == right_index:
                self.s_r_mm = ModulusMaxima(right_index, self.r_mms[0].id, wdc)
            else:
                right_mm_index = self.index + np.argmax(np.abs(wdc[self.index:right_index]))
                self.s_r_mm = ModulusMaxima(right_mm_index, self.r_mms[0].id, wdc)

        self.s_ampl = abs(self.s_l_mm.value) + abs(self.s_r_mm.value)