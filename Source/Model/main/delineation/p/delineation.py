"""
Точка входа алгоритма сегментации зубца P.

Входные параметры:
    ecg_lead - экземпляр класса отведения сигнала ЭКГ.
"""

from Source.Model.main.delineation.wave_delineation import WaveSpecification
from Source.Model.main.delineation.p.alpha.alpha import get_p_del
from Source.Model.main.delineation.p.beta.beta import get_p_morph


def get_p_dels(ecg_lead):

    dels = []
    morphs = []
    num_dels = 0

    for qrs_id in range(1, len(ecg_lead.qrs_dels)):

        delineation = get_p_del(ecg_lead, qrs_id)

        if delineation.specification is not WaveSpecification.absence:
            morphology = get_p_morph(ecg_lead, num_dels, delineation)
            dels.append(delineation)
            morphs.append(morphology)
            num_dels += 1

    return dels, morphs

