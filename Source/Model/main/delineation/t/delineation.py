"""
Точка входа алгоритма сегментации зубца T.

Входные параметры:
    ecg_lead - экземпляр класса отведения сигнала ЭКГ.
    qrs_id - индекс текущего комплекса QRS.
"""

from Source.Model.main.delineation.t.zcs import *
from Source.Model.main.delineation.t.peak import *
from Source.Model.main.delineation.peaks_zcs_ids import *
from Source.Model.main.delineation.t.onset import *
from Source.Model.main.delineation.t.offset import *
from Source.Model.main.delineation.t.routines import *


class InvalidPDelineation(Exception):
    pass


def get_t_delineations(ecg_lead):

    delineations = []

    for qrs_id in range(1, len(ecg_lead.cur_qrs_dels_seq)):

        delineation = get_t_delineation(ecg_lead, qrs_id)

        if delineation.specification is not WaveSpecification.absence:
            delineations.append(delineation)

    return delineations


def get_t_delineation(ecg_lead, qrs_id):

    sampling_rate = ecg_lead.sampling_rate

    delineation = WaveDelineation()

    mm_window = int(float(TParams['MM_WINDOW']) * sampling_rate)

    qrs_gap = ecg_lead.cur_qrs_dels_seq[qrs_id].peak_index - ecg_lead.cur_qrs_dels_seq[qrs_id - 1].peak_index
    shift = int(float(TParams['BEGIN_SHIFT']) * sampling_rate)
    if shift >= qrs_gap:
        return delineation

    zcs = get_t_zcs(ecg_lead, qrs_id, mm_window)

    if not zcs:
        return delineation

    if abs(zcs[0].left_mm.value) / abs(zcs[0].right_mm.value) > float(TParams['MM_SHARPNESS']):
        zcs.pop(0)

    if not zcs:
        return delineation

    begin_index = get_t_begin_index(ecg_lead, qrs_id)
    end_index = get_t_end_index(ecg_lead, qrs_id)

    peak_zc_id = get_t_peak_zc_id(ecg_lead, qrs_id, zcs)

    peak_zc = zcs[peak_zc_id]
    peak_index = peak_zc.index
    delineation.peak_index = peak_index
    delineation.specification = WaveSpecification.normal

    peak_zcs_ids = PeakZCsIds(peak_zc_id, peak_zc_id, peak_zc_id)

    peak_zcs_ids.check_flexure_t(ecg_lead, qrs_id, zcs, delineation)
    peak_zcs_ids.check_left_biphasic_t(ecg_lead, qrs_id, zcs, delineation)
    peak_zcs_ids.check_right_biphasic_t(ecg_lead, qrs_id, zcs, delineation)

    define_t_onset_index(ecg_lead, delineation, zcs, peak_zcs_ids.left_zc_id, begin_index)
    define_t_offset_index(ecg_lead, delineation, zcs, peak_zcs_ids.right_zc_id, end_index)

    return delineation

