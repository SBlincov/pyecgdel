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
        self.keys = []

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
        self.g_l_mm = self.l_mms[np.argmax(abs(mm.value) for mm in self.l_mms)] if len(self.l_mms) > 0 else None
        self.g_r_mm = self.r_mms[np.argmax(abs(mm.value) for mm in self.r_mms)] if len(self.r_mms) > 0 else None
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



    def special(self, l_window, r_window):
        l_mms = [mm for mm in self.l_mms if mm.index > self.index - l_window]
        r_mms = [mm for mm in self.r_mms if mm.index < self.index + r_window]

        self.s_l_mm = l_mms[np.argmax(abs(mm.value) for mm in l_mms)] if len(l_mms) > 0 else None
        self.s_r_mm = r_mms[np.argmax(abs(mm.value) for mm in r_mms)] if len(r_mms) > 0 else None
        if self.s_l_mm is not None and self.s_r_mm is not None:
            self.s_ampl = abs(self.s_l_mm.value) + abs(self.s_r_mm.value)

