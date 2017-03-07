"""
Алгорим поиска пика T.

Входные параметры:
    ecg_lead - экземпляр класса отведения сигнала ЭКГ.
    qrs_id - индекс текущего комплекса QRS.
    zcs - список пересечений нуля детализирующими вейвлет-коэффициентами.
    peak_zc_id - индекс пересечения нуля, соотвествующий пику комплекса.
"""

from Source.Model.main.params.t import *
from Source.Model.main.ecg_lead.ecg_lead import *
from Source.Model.main.modulus_maxima.routines import *
from Source.Model.main.delineation.t.routines import *


def is_t_peak_zc_candidate_exist(ecg_lead, qrs_id, zcs):

    sampling_rate = ecg_lead.sampling_rate

    begin_index = get_t_begin_index(ecg_lead, qrs_id)
    end_index = get_t_end_index(ecg_lead, qrs_id)

    zcs_peaks_candidates_begin_index = begin_index
    zcs_peaks_candidates_end_index = end_index + int(float(TParams['PEAK_END_PROPORTION']) * sampling_rate)

    result = False

    for zc in zcs:
        if zcs_peaks_candidates_begin_index < zc.index < zcs_peaks_candidates_end_index:
            result = True
            break

    return result


def get_t_peak_zc_id(ecg_lead, qrs_id, zcs):

    cur_qrs_dels_seq = ecg_lead.cur_qrs_dels_seq

    rr = cur_qrs_dels_seq[qrs_id].peak_index - cur_qrs_dels_seq[qrs_id - 1].peak_index

    begin_index = get_t_begin_index(ecg_lead, qrs_id)
    end_index = get_t_end_index(ecg_lead, qrs_id)

    zcs_peaks_candidates_begin_index = begin_index
    zcs_peaks_candidates_end_index = min(begin_index + rr * float(TParams['PEAK_END_PROPORTION']), end_index)
    zcs_peaks_candidates_window = zcs_peaks_candidates_end_index - zcs_peaks_candidates_begin_index
    zcs_peaks_candidates_point = zcs_peaks_candidates_begin_index + zcs_peaks_candidates_window / 3

    peak_zc_id = 0
    peak_zc_mm_amplitude = 0.0

    for candidate_zc_id in range(len(zcs)):
        if zcs_peaks_candidates_begin_index < zcs[candidate_zc_id].index < zcs_peaks_candidates_end_index:

            shift_percentage = abs(float(zcs[candidate_zc_id].index - zcs_peaks_candidates_point)) / float(zcs_peaks_candidates_window)
            amplitude_part = 1.0 - shift_percentage * float(TParams['AMPLITUDE_DECREASING'])

            if zcs[candidate_zc_id].mm_amplitude * amplitude_part >= peak_zc_mm_amplitude:
                peak_zc_id = candidate_zc_id
                peak_zc_mm_amplitude = zcs[candidate_zc_id].mm_amplitude * amplitude_part

    return peak_zc_id


def get_t_flexure_zc_id(ecg_lead, qrs_id, zcs, peak_zc_id):

    cur_qrs_dels_seq = ecg_lead.cur_qrs_dels_seq

    flexure_zc_id = -1

    rr = cur_qrs_dels_seq[qrs_id].peak_index - cur_qrs_dels_seq[qrs_id - 1].peak_index

    begin_index = get_t_begin_index(ecg_lead, qrs_id)
    end_index = get_t_end_index(ecg_lead, qrs_id)

    zcs_peaks_candidates_begin_index = begin_index
    zcs_peaks_candidates_end_index = min(begin_index + rr * float(TParams['PEAK_END_PROPORTION']), end_index)
    zcs_peaks_candidates_window = zcs_peaks_candidates_end_index - zcs_peaks_candidates_begin_index

    for zc_id in range(1, len(zcs) - 1):
        if zcs_peaks_candidates_begin_index + zcs_peaks_candidates_window * 0.15 < \
                zcs[zc_id].index < zcs_peaks_candidates_end_index - zcs_peaks_candidates_window * 0.40:
            if abs(zcs[zc_id - 1].index - zcs[zc_id].index) < float(TParams['FLEXURE_SHIFT']) * rr \
                    and abs(zcs[zc_id + 1].index - zcs[zc_id].index) < float(TParams['FLEXURE_SHIFT']) * rr \
                    and zcs[zc_id].mm_amplitude < float(TParams['FLEXURE_AMPLITUDE']) * zcs[zc_id - 1].mm_amplitude \
                    and zcs[zc_id].mm_amplitude < float(TParams['FLEXURE_AMPLITUDE']) * zcs[zc_id + 1].mm_amplitude\
                    and zcs[zc_id - 1].mm_amplitude > float(TParams['LITTLE_AMPLITUDE_COMP']) * zcs[peak_zc_id].mm_amplitude\
                    and zcs[zc_id + 1].mm_amplitude > float(TParams['LITTLE_AMPLITUDE_COMP']) * zcs[peak_zc_id].mm_amplitude:
                flexure_zc_id = zc_id

    return flexure_zc_id
