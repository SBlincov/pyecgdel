"""
Класс пересечений нуля детализирующими вейвлет-коэффициентами.
"""

import numpy as np
from ..modulus_maxima.routines import *


class InvalidZeroCrossingData(Exception):
    pass


class ZeroCrossing:
    def __init__(self, index, wdc):
        self.index = index
        self.right_mm = ModulusMaxima(index, wdc)
        self.left_mm = ModulusMaxima(index, wdc)
        self.mm_amplitude = 0.0

    def init_global_mm_right(self, right_border_index, wdc):
        right_mm_index = self.index + np.argmax(np.abs(wdc[self.index:right_border_index]))
        self.right_mm = ModulusMaxima(right_mm_index, wdc)

        self.mm_amplitude = abs(self.left_mm.value) + abs(self.right_mm.value)

    def init_global_mm_left(self, left_border_index, wdc):
        left_mm_index = left_border_index + np.argmax(np.abs(wdc[left_border_index:self.index]))
        self.left_mm = ModulusMaxima(left_mm_index, wdc)

        self.mm_amplitude = abs(self.left_mm.value) + abs(self.right_mm.value)

    def init_local_mm_right(self, right_border_index, wdc):
        candidate_mm = find_right_mm(self.index, wdc)
        if candidate_mm.index < right_border_index:
            self.right_mm = candidate_mm
        else:
            self.right_mm = ModulusMaxima(right_border_index, wdc)

        self.mm_amplitude = abs(self.left_mm.value) + abs(self.right_mm.value)

    def init_local_mm_left(self, left_border_index, wdc):
        candidate_mm = find_left_mm(self.index, wdc)
        if candidate_mm.index > left_border_index:
            self.left_mm = candidate_mm
        else:
            self.left_mm = ModulusMaxima(left_border_index, wdc)

        self.mm_amplitude = abs(self.left_mm.value) + abs(self.right_mm.value)

    def init_special_mm_right(self, right_border_index, wdc):
        current_mm = find_right_mm(self.index, wdc)
        if current_mm.index >= right_border_index - 1:
            right_mm_index = self.index + np.argmax(np.abs(wdc[self.index:right_border_index]))
            self.right_mm = ModulusMaxima(right_mm_index, wdc)
        else:
            candidate_mm = current_mm
            while current_mm.index < right_border_index - 1:
                if abs(current_mm.value) > abs(candidate_mm.value):
                    candidate_mm = current_mm
                current_mm = find_right_mm(current_mm.index + 1, wdc)

            self.right_mm = candidate_mm

        self.mm_amplitude = abs(self.left_mm.value) + abs(self.right_mm.value)

    def init_special_mm_left(self, left_border_index, wdc):
        current_mm = find_left_mm(self.index, wdc)
        if current_mm.index <= left_border_index + 1:
            left_mm_index = left_border_index + np.argmax(np.abs(wdc[left_border_index:self.index]))
            self.left_mm = ModulusMaxima(left_mm_index, wdc)
        else:
            candidate_mm = current_mm
            while current_mm.index > left_border_index + 1:
                if abs(current_mm.value) > abs(candidate_mm.value):
                    candidate_mm = current_mm
                current_mm = find_left_mm(current_mm.index - 1, wdc)

            self.left_mm = candidate_mm

        self.mm_amplitude = abs(self.left_mm.value) + abs(self.right_mm.value)