"""
Точка входа алгоритма сегментации комплекса QRS.

Входные параметры:
    ecg_lead - экземпляр класса отведения сигнала ЭКГ.
    start_index - левая граница поиска.
    end_index - правая граница поиска.
    qrs_zc_id - индекс пересечения нуля детализирующими вейвлет-коэффициентами для текущего комплекса QRS.
    qrs_zcs - список пересечений нуля детализирующими вейвлет-коэффициентами.
"""

from Source.Model.main.delineation.qrs.onset import *
from Source.Model.main.delineation.qrs.offset import *
from Source.Model.main.delineation.qrs.peak import *
from Source.Model.main.delineation.qrs.zcs import *
from Source.Model.main.delineation.qrs.routines import *
from Source.Model.main.params.qrs import *
from Source.Model.main.delineation.qrs.morphology import *


class InvalidQRSDelineation(Exception):
    pass


def get_qrs_delineations(ecg_lead, start_index, end_index):

    wdc = ecg_lead.wdc
    wdc_scale_id = get_qrs_wdc_scale_id(ecg_lead)
    aux_wdc_scale_id = get_qrs_aux_wdc_scale_id(ecg_lead)

    qrs_zcs = get_zcs_with_global_mms(wdc[wdc_scale_id], start_index, end_index)

    qrs_zcs_ids = get_qrs_zcs_ids(ecg_lead, wdc_scale_id, aux_wdc_scale_id, qrs_zcs)

    delineations = []
    morphologies = []
    num_dels = 0
    for qrs_zc_id in qrs_zcs_ids:
        delineation = get_qrs_delineation(ecg_lead, qrs_zc_id, qrs_zcs)
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


def get_qrs_delineation(ecg_lead, qrs_zc_id, qrs_zcs):

    delineation = WaveDelineation()

    # define qrs peak index for WaveDelineation instance
    define_qrs_peak_index(ecg_lead, delineation, qrs_zc_id, qrs_zcs)

    # define qrs onset index for WaveDelineation instance
    define_qrs_onset_index(ecg_lead, delineation, qrs_zc_id, qrs_zcs)

    # define qrs offset index for WaveDelineation instance
    define_qrs_offset_index(ecg_lead, delineation, qrs_zc_id, qrs_zcs)

    return delineation


