"""
Класс экстремума детализирующего вейвлет-коэффициента.
"""

import numpy as np

class ModulusMaxima:

    def __init__(self, index, wdc):
        self.index = index
        self.set_value(wdc)
        self.set_correctness(wdc)

    def set_correctness(self, wdc):

        if self.index == 0:
            if ((wdc[self.index] > wdc[self.index + 1]) and (wdc[self.index] > 0)) \
                    or ((wdc[self.index] < wdc[self.index + 1]) and (wdc[self.index] < 0)):
                self.correctness = True
            else:
                self.correctness = False

        elif self.index == len(wdc) - 1:
            if ((wdc[self.index] > wdc[self.index - 1]) and (wdc[self.index] > 0)) \
                    or ((wdc[self.index] < wdc[self.index - 1]) and (wdc[self.index] < 0)):
                self.correctness = True
            else:
                self.correctness = False

        else:
            if ((wdc[self.index] > wdc[self.index + 1]) and (wdc[self.index] > wdc[self.index - 1]) and (wdc[self.index] > 0)) \
                    or ((wdc[self.index] < wdc[self.index + 1]) and (wdc[self.index] < wdc[self.index - 1]) and (wdc[self.index] < 0)):
                self.correctness = True
            else:
                self.correctness = False

    def set_value(self, wdc):
        self.value = wdc[self.index]

