"""
Точка входа алгоритма сегментации комплекса QRS.

Входные параметры:
    ecg_lead - экземпляр класса отведения сигнала ЭКГ.
    start_index - левая граница поиска.
    end_index - правая граница поиска.
    qrs_zc_id - индекс пересечения нуля детализирующими вейвлет-коэффициентами для текущего комплекса QRS.
    qrs_zcs - список пересечений нуля детализирующими вейвлет-коэффициентами.
"""
from Source.Model.main.delineation.qrs.beta.beta import beta_processing
from Source.Model.main.delineation.qrs.gamma.gamma import *


def get_qrs_dels(ecg_lead, begin_index, end_index):

    qrs_zcs = alpha_processing(ecg_lead, begin_index, end_index)

    delineations = []
    morphologies = []
    num_dels = 0
    for qrs_zc in qrs_zcs:
        delineation = beta_processing(ecg_lead, qrs_zc)
        morphology = get_qrs_morphology(ecg_lead, num_dels, delineation)
        delineations.append(delineation)
        morphologies.append(morphology)
        num_dels += 1

    mean_rr = 0.0

    for qrs_delineation_id in range(0, len(delineations) - 1):
        mean_rr += (delineations[qrs_delineation_id + 1].peak_index - delineations[qrs_delineation_id].peak_index)

    if len(delineations) > 1:
        mean_rr /= (len(delineations) - 1)

    for qrs_delineation_id in range(1, len(delineations)):
        rr = (delineations[qrs_delineation_id].peak_index - delineations[qrs_delineation_id - 1].peak_index)
        if rr < float(QRSParams['EXTRA_BEAT_PART']) * mean_rr:
            delineations[qrs_delineation_id].specification = WaveSpecification.extra

    return delineations, morphologies


