"""
Точка входа алгоритма сегментации зубца P.

Входные параметры:
    ecg_lead - экземпляр класса отведения сигнала ЭКГ.
    qrs_id - индекс текущего комплекса QRS.
    delineation - экземпляр класса, содержащего информацию о текущем сегментированном комплексе.
    zcs - список пересечений нуля детализирующими вейвлет-коэффициентами.
    peak_zc_id - индекс пересечения нуля, соотвествующий пику комплекса.
"""

from Source.Model.main.delineation.p.alpha.alpha import get_p_del
from Source.Model.main.delineation.peaks_zcs_ids import *
from Source.Model.main.delineation.p.zcs import *
from Source.Model.main.delineation.p.routines import *

import numpy as np


def get_p_dels(ecg_lead):

    dels = []
    morphs = []

    for qrs_id in range(1, len(ecg_lead.qrs_dels)):

        delineation = get_p_del(ecg_lead, qrs_id)

        if delineation.specification is not WaveSpecification.absence:
            dels.append(delineation)

    return dels, morphs




