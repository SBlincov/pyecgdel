"""
Точка входа алгоритма сегментации зубца T.

Входные параметры:
    ecg_lead - экземпляр класса отведения сигнала ЭКГ.
    qrs_id - индекс текущего комплекса QRS.
"""

from Source.Model.main.delineation.peaks_zcs_ids import WaveSpecification
from Source.Model.main.delineation.t.alpha.alpha import get_t_delineation
from Source.Model.main.delineation.t.beta.beta import get_t_morphology


class InvalidPDelineation(Exception):
    pass


def get_t_delineations(ecg_lead):

    delineations = []
    morphologies = []
    num_dels = 0

    for qrs_id in range(1, len(ecg_lead.cur_qrs_dels_seq)):

        delineation = get_t_delineation(ecg_lead, qrs_id)

        if delineation.specification is not WaveSpecification.absence:
            morphology = get_t_morphology(ecg_lead, num_dels, delineation)
            delineations.append(delineation)
            morphologies.append(morphology)
            num_dels += 1

    return delineations, morphologies


