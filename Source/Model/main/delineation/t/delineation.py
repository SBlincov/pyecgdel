"""
Точка входа алгоритма сегментации зубца T.

Входные параметры:
    ecg_lead - экземпляр класса отведения сигнала ЭКГ.
    qrs_id - индекс текущего комплекса QRS.
"""

from Source.Model.main.delineation.peaks_zcs_ids import *
from Source.Model.main.delineation.t.zcs import *
from Source.Model.main.delineation.t.alpha.alpha import *


class InvalidPDelineation(Exception):
    pass


def get_t_delineations(ecg_lead):

    delineations = []
    morphologies = []

    for qrs_id in range(1, len(ecg_lead.cur_qrs_dels_seq)):

        delineation = get_t_delineation(ecg_lead, qrs_id)

        if delineation.specification is not WaveSpecification.absence:
            delineations.append(delineation)

    return delineations


