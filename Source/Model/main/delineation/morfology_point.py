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
    qrs_offset = "qrs_offset"

    t_onset = "t_onset"
    t_peak = "t_peak"
    t_offset = "t_offset"

    xtd_point = "xtd_point"

    def __str__(self):
        return str(self.value)


class WaveSign(Enum):
    negative = -1
    positive = 1
    none = 0

    def __int__(self):
        return self.value


class Degree(Enum):
    satisfyingly = 0
    doubtfully = 1
    unknown = 2

    def __int__(self):
        return self.value
