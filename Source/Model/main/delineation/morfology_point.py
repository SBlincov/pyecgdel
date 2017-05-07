"""
Перечисление основных морфологий комплексов.
"""

from enum import Enum


class Point:

    def __init__(self, name, index, value, sign):
        self.name = name
        self.index = index
        self.value = value
        self.sign = sign


class PointName(Enum):
    qrs_onset = "qrs_onset"
    q = "q"
    r = "r"
    s = "s"
    r_hatch = "r'"
    qrs_offset = "qrs_offset"
    xtd_point = "xtd_point"

    def __str__(self):
        return str(self.value)


class WaveSign(Enum):
    negative = -1
    positive = 1
    none = 0

    def __int__(self):
        return self.value