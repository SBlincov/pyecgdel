"""
Служебный файл, определяюший суффиксы локально сохраняемых данных
"""

from enum import Enum


class InvalidECGDataDetails(Exception):
    pass


class ECGDataDetails(Enum):
    original = 'original'
    filtrated = 'filtrated'
    wdc = 'wdc'
    qrs_delineation = 'qrs_delineation'
    qrs_morphology = 'qrs_morphology'
    p_delineation = 'p_delineation'
    t_delineation = 't_delineation'
    characteristics = 'characteristics'

    def __str__(self):
        return self.value
