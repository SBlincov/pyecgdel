"""
Вспомогательная структура для распознавания различных морфологий комплексов.
"""

from Source.Model.main.delineation.wave_delineation import WaveSpecification
from Source.Model.main.params.p import PParams
from Source.Model.main.params.t import TParams


class PeakZCsIds:

    def __init__(self, left_zc_id, center_zc_id, right_zc_id):
        self.left_zc_id = left_zc_id
        self.center_zc_id = center_zc_id
        self.right_zc_id = right_zc_id


def is_prev_zc_exist(zcs, zc_id, window):

    result = False

    if zc_id > 0:
        if (zcs[zc_id].index - zcs[zc_id - 1].index) < window:
            result = True

    return result


def is_next_zc_exist(zcs, zc_id, window):

    result = False

    if zc_id < len(zcs) - 1:
        if (zcs[zc_id + 1].index - zcs[zc_id].index) < window:
            result = True

    return result


def distance_between_zcs(zcs, zc_id_left, zc_id_right):
    return zcs[zc_id_right].index - zcs[zc_id_left].index
