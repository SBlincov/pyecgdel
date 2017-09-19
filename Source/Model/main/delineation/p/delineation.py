"""
Точка входа алгоритма сегментации зубца P.

Входные параметры:
    ecg_lead - экземпляр класса отведения сигнала ЭКГ.
    qrs_id - индекс текущего комплекса QRS.
    delineation - экземпляр класса, содержащего информацию о текущем сегментированном комплексе.
    zcs - список пересечений нуля детализирующими вейвлет-коэффициентами.
    peak_zc_id - индекс пересечения нуля, соотвествующий пику комплекса.
"""

from Source.Model.main.delineation.p.offset import *
from Source.Model.main.delineation.p.peak import *
from Source.Model.main.delineation.p.onset import *
from Source.Model.main.delineation.peaks_zcs_ids import *
from Source.Model.main.delineation.p.zcs import *
from Source.Model.main.delineation.p.routines import *

import numpy as np


class InvalidPDelineation(Exception):
    pass


def get_p_delineations(ecg_lead):

    delineations = []

    for qrs_id in range(1, len(ecg_lead.cur_qrs_dels_seq)):

        delineation = get_p_delineation(ecg_lead, qrs_id)

        if delineation.specification is not WaveSpecification.absence:
            delineations.append(delineation)

    return delineations


def get_p_delineation(ecg_lead, qrs_id):

    delineation = WaveDelineation()

    if ecg_lead.cur_qrs_dels_seq[qrs_id].specification is WaveSpecification.extra:
        return delineation

    sampling_rate = ecg_lead.sampling_rate

    mm_window = int(float(PParams['MM_WINDOW']) * sampling_rate)

    zcs = get_p_zcs(ecg_lead, qrs_id, mm_window)

    if not zcs:
        return delineation

    if ((zcs[-1].right_mm.index - zcs[-1].index) > int(float(PParams['RIGHT_MM_DIST']) * sampling_rate)) or (abs(zcs[-1].right_mm.value) / abs(zcs[-1].left_mm.value) > float(PParams['OFFSET_MM_SHARPNESS'])):
        zcs.pop(-1)

    if not zcs:
        return delineation

    if ((zcs[0].index - zcs[0].left_mm.index) > int(float(PParams['LEFT_MM_DIST']) * sampling_rate)) or (abs(zcs[0].left_mm.value) / abs(zcs[0].right_mm.value) > float(PParams['ONSET_MM_SHARPNESS'])):
        zcs.pop(0)

    if not zcs:
        return delineation

    window = get_window(ecg_lead, qrs_id)
    begin_index = get_p_begin_index(ecg_lead, qrs_id)
    end_index = get_p_end_index(ecg_lead, qrs_id)

    if window < int(float(PParams['ZCS_PEAK_SEARCHING_SHIFT']) * sampling_rate):
        return delineation

    if not is_p_peak_zc_candidate_exist(ecg_lead, qrs_id, zcs):
        return delineation

    peak_zc_id = get_p_peak_zc_id(ecg_lead, qrs_id, zcs)

    if is_small_p(ecg_lead, qrs_id, zcs, peak_zc_id):
        return delineation

    peak_zc = zcs[peak_zc_id]
    peak_index = peak_zc.index
    delineation.peak_index = peak_index
    delineation.specification = WaveSpecification.exist

    peak_zcs_ids = PeakZCsIds(peak_zc_id, peak_zc_id, peak_zc_id)

    peak_zcs_ids.check_flexure_p(ecg_lead, qrs_id, zcs, delineation)

    peak_zcs_ids.check_left_biphasic_p(ecg_lead, zcs, delineation)

    define_p_onset_index(ecg_lead, delineation, zcs, peak_zcs_ids.left_zc_id, begin_index)
    define_p_offset_index(ecg_lead, delineation, zcs, peak_zcs_ids.right_zc_id, end_index)

    check_for_atrial_fibrillation(delineation, zcs)

    return delineation


def check_for_atrial_fibrillation(delineation, zcs):

    zcs_amplitudes = []
    for zc in zcs:
        zcs_amplitudes.append(zc.mm_amplitude)

    zcs_amplitudes = np.asarray(zcs_amplitudes)

    if len(zcs) > int(PParams['FIB_NUM_ZCS']):

        zcs_amplitudes = np.sort(zcs_amplitudes)[::-1]
        zcs_amplitudes = zcs_amplitudes[1:int(PParams['FIB_NUM_ZCS']) + 1]

        zcs_amplitudes_mean = np.mean(zcs_amplitudes)
        zcs_amplitudes_std = np.std(zcs_amplitudes)

        if zcs_amplitudes_std < zcs_amplitudes_mean * float(PParams['FIB_STD']):
            delineation.specification = WaveSpecification.atrial_fibrillation


def is_small_p(ecg_lead, qrs_id, zcs, peak_zc_id):

    answer = False

    wdc_scale_id = get_p_wdc_scale_id(ecg_lead)
    wdc = ecg_lead.wdc[wdc_scale_id]
    p_amplitude = zcs[peak_zc_id].mm_amplitude
    begin_qrs_index = ecg_lead.cur_qrs_dels_seq[qrs_id].onset_index
    end_qrs_index = ecg_lead.cur_qrs_dels_seq[qrs_id].offset_index
    qrs_aux_zcs = get_zcs_with_global_mms(wdc, begin_qrs_index, end_qrs_index)
    if qrs_aux_zcs:

        qrs_zc = qrs_aux_zcs[0]

        for qrs_zc_candidate in qrs_aux_zcs[1:]:
            if qrs_zc_candidate.mm_amplitude > qrs_zc.mm_amplitude:
                qrs_zc = qrs_zc_candidate

        qrs_amplitude = qrs_zc.mm_amplitude

        if p_amplitude < float(PParams['LOW_LIMIT_AMPLITUDE']) * qrs_amplitude:
            answer = True

    return answer





