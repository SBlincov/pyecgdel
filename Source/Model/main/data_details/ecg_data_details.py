"""
Служебный файл, определяюший суффиксы локально сохраняемых данных
"""

from enum import Enum


class InvalidECGDataDetails(Exception):
    pass


class ECGDataDetails(Enum):
    original = 'original'
    filtrated = 'filtrated'
    adaptive_filtrated = 'adaptive_filtrated'
    wdc = 'wdc'
    qrs_delineation = 'qrs_delineation'
    qrs_morphology = 'qrs_morphology'
    p_delineation = 'p_delineation'
    p_morphology = 'p_morphology'
    t_delineation = 't_delineation'
    t_morphology = 't_morphology'
    characteristics = 'characteristics'
    qrs_plot_data = 'qrs_plot_data'

    def __str__(self):
        return self.value
