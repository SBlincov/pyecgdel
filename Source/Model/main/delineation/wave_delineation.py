"""
Перечисление основных морфологий комплексов.
"""

from enum import Enum


class InvalidWaveletProcessing(Exception):
    pass


class WaveSpecification(Enum):
    absence = 0
    exist = 1
    biphasic = 2
    flexure = 3
    extra = 5
    atrial_fibrillation = 6

    def __int__(self):
        return self.value


class WaveDelineation:

    def __init__(self, specification=WaveSpecification.absence):
        self.onset_index = 0
        self.peak_index = 0
        self.offset_index = 0
        self.special_points_indexes = []
        self.specification = specification


class Morphology:

    def __init__(self, del_id, points, degree, branch_id):
        self.del_id = del_id
        self.points = points
        self.degree = degree
        self.branch_id = branch_id




