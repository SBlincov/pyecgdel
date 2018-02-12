"""
Алгорим поиска пика P.

Входные параметры:
    ecg_lead - экземпляр класса отведения сигнала ЭКГ.
    qrs_id - индекс текущего комплекса QRS.
    zcs - список пересечений нуля детализирующими вейвлет-коэффициентами.
    peak_zc_id - индекс пересечения нуля, соотвествующий пику комплекса.
"""

from Source.Model.main.params.p_default import *
from Source.Model.main.ecg_lead.ecg_lead import *
from Source.Model.main.modulus_maxima.routines import *
from Source.Model.main.delineation.p.routines import *


def is_p_peak_zc_candidate_exist(ecg_lead, qrs_id, zcs):

    sampling_rate = ecg_lead.sampling_rate

    begin_index = get_p_begin_index(ecg_lead, qrs_id)
    end_index = get_p_end_index(ecg_lead, qrs_id)

    zcs_peaks_candidates_begin_index = begin_index + int(float(PParams['ZCS_PEAK_SEARCHING_SHIFT']) * sampling_rate)
    zcs_peaks_candidates_end_index = end_index

    result = False

    for zc in zcs:
        if zcs_peaks_candidates_begin_index < zc.index < zcs_peaks_candidates_end_index:
            result = True
            break

    return result


def get_p_peak_zc_id(ecg_lead, qrs_id, zcs):

    sampling_rate = ecg_lead.sampling_rate

    begin_index = get_p_begin_index(ecg_lead, qrs_id)
    end_index = get_p_end_index(ecg_lead, qrs_id)

    zcs_peaks_candidates_begin_index = begin_index + int(float(PParams['ZCS_PEAK_SEARCHING_SHIFT']) * sampling_rate)
    zcs_peaks_candidates_end_index = end_index

    candidates_zcs_ids = []
    for candidate_zc_id in range(len(zcs)):
        if zcs_peaks_candidates_begin_index < zcs[candidate_zc_id].index < zcs_peaks_candidates_end_index:
            candidates_zcs_ids.append(candidate_zc_id)

    if len(candidates_zcs_ids) is 1:
        peak_zc_id = candidates_zcs_ids[0]
        return peak_zc_id

    zcs_candidates_begin_index = zcs[candidates_zcs_ids[0]].index - int((zcs[candidates_zcs_ids[0]].index - zcs_peaks_candidates_begin_index) * PParams['PEAK_ZC_AMPLITUDE_DECREASING_LEFT_PRIVILEGE'])
    zcs_candidates_end_index = zcs[candidates_zcs_ids[-1]].index + int((zcs_peaks_candidates_end_index - zcs[candidates_zcs_ids[-1]].index) * PParams['PEAK_ZC_AMPLITUDE_DECREASING_RIGHT_PRIVILEGE'])
    zcs_peaks_candidates_window = zcs_candidates_end_index - zcs_candidates_begin_index
    begin_part = float(PParams['PEAK_ZC_AMPLITUDE_DECREASING_BEGIN_PART'])
    end_part = 1.0 - begin_part
    zcs_peaks_candidates_point = zcs_candidates_begin_index + zcs_peaks_candidates_window * begin_part

    peak_zc_id = 0
    peak_zc_mm_amplitude = 0.0

    for candidate_zc_id in candidates_zcs_ids:

        shift_percentage = float(zcs[candidate_zc_id].index - zcs_peaks_candidates_point)
        if shift_percentage < 0.0:
            shift_percentage = abs(shift_percentage) / (zcs_peaks_candidates_window * begin_part)
        else:
            shift_percentage = abs(shift_percentage) / (zcs_peaks_candidates_window * end_part)

        amplitude_part = 1.0 - pow(shift_percentage, float(PParams['PEAK_ZC_AMPLITUDE_DECREASING_POW'])) * float(PParams['PEAK_ZC_AMPLITUDE_DECREASING'])

        if zcs[candidate_zc_id].mm_amplitude * amplitude_part >= peak_zc_mm_amplitude:
            peak_zc_id = candidate_zc_id
            peak_zc_mm_amplitude = zcs[candidate_zc_id].mm_amplitude * amplitude_part

    return peak_zc_id


def get_p_flexure_zc_id(ecg_lead, qrs_id, zcs, peak_zc_id):

    cur_qrs_dels_seq = ecg_lead.cur_qrs_dels_seq

    flexure_zc_id = -1

    rr = cur_qrs_dels_seq[qrs_id].peak_index - cur_qrs_dels_seq[qrs_id - 1].peak_index

    for zc_id in range(1, len(zcs) - 1):
        if abs(zcs[zc_id - 1].index - zcs[zc_id].index) < float(PParams['FLEXURE_SHIFT']) * rr \
                and abs(zcs[zc_id + 1].index - zcs[zc_id].index) < float(PParams['FLEXURE_SHIFT']) * rr \
                and zcs[zc_id].mm_amplitude < float(PParams['FLEXURE_AMPLITUDE_NEIGHBOUR']) * zcs[zc_id - 1].mm_amplitude \
                and zcs[zc_id].mm_amplitude < float(PParams['FLEXURE_AMPLITUDE_NEIGHBOUR']) * zcs[zc_id + 1].mm_amplitude\
                and zcs[zc_id - 1].mm_amplitude > float(PParams['FLEXURE_AMPLITUDE_OLD_ZC']) * zcs[peak_zc_id].mm_amplitude\
                and zcs[zc_id + 1].mm_amplitude > float(PParams['FLEXURE_AMPLITUDE_OLD_ZC']) * zcs[peak_zc_id].mm_amplitude:
            flexure_zc_id = zc_id

    return flexure_zc_id
