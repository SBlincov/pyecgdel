"""
Алгорим поиска пика P.

Входные параметры:
    ecg_lead - экземпляр класса отведения сигнала ЭКГ.
    qrs_id - индекс текущего комплекса QRS.
    zcs - список пересечений нуля детализирующими вейвлет-коэффициентами.
    peak_zc_id - индекс пересечения нуля, соотвествующий пику комплекса.
"""

from Source.Model.main.params.p import PParams
from Source.Model.main.ecg_lead.ecg_lead import *
from Source.Model.main.modulus_maxima.routines import *
from Source.Model.main.delineation.p.routines import *


def is_small_p(ecg_lead, qrs_id, zcs, peak_zc_id):
    result = False

    wdc_scale_id = get_p_wdc_scale_id(ecg_lead)
    p_amplitude = zcs[peak_zc_id].s_ampl
    begin_qrs_index = ecg_lead.qrs_dels[qrs_id].onset_index
    end_qrs_index = ecg_lead.qrs_dels[qrs_id].offset_index
    qrs_aux_zcs = get_zcs_in_window(ecg_lead.wdc[wdc_scale_id], ecg_lead.zcs[wdc_scale_id], ecg_lead.ids_zcs[wdc_scale_id], begin_qrs_index, end_qrs_index)

    if qrs_aux_zcs:
        qrs_zc = qrs_aux_zcs[0]
        for qrs_zc_candidate in qrs_aux_zcs[1:]:
            if qrs_zc_candidate.g_ampl > qrs_zc.g_ampl:
                qrs_zc = qrs_zc_candidate

        qrs_amplitude = qrs_zc.g_ampl

        if p_amplitude < float(PParams['ALPHA_PEAK_SMALL_AMPL']) * qrs_amplitude:
            result = True

    return result

def is_p_peak_zc_candidate_exist(ecg_lead, qrs_id, zcs):

    rate = ecg_lead.rate

    begin_index = get_p_begin_index(ecg_lead, qrs_id)
    end_index = get_p_end_index(ecg_lead, qrs_id)

    zcs_peaks_candidates_begin_index = begin_index + int(float(PParams['ALPHA_PEAK_BEGIN_SHIFT']) * rate)
    zcs_peaks_candidates_end_index = end_index

    result = False

    for zc in zcs:
        if zcs_peaks_candidates_begin_index < zc.index < zcs_peaks_candidates_end_index:
            result = True
            break

    return result


def get_p_peak_zc_id(ecg_lead, qrs_id, zcs):

    rate = ecg_lead.rate

    begin_index = get_p_begin_index(ecg_lead, qrs_id)
    end_index = get_p_end_index(ecg_lead, qrs_id)

    zcs_peaks_cands_begin_index = begin_index + int(float(PParams['ALPHA_PEAK_BEGIN_SHIFT']) * rate)
    zcs_peaks_cands_end_index = end_index

    cands_zcs_ids = []
    for cand_zc_id in range(len(zcs)):
        if zcs_peaks_cands_begin_index < zcs[cand_zc_id].index < zcs_peaks_cands_end_index:
            cands_zcs_ids.append(cand_zc_id)

    if len(cands_zcs_ids) is 1:
        peak_zc_id = cands_zcs_ids[0]
        return peak_zc_id

    zcs_cands_begin_index = zcs[cands_zcs_ids[0]].index - int((zcs[cands_zcs_ids[0]].index - zcs_peaks_cands_begin_index) * PParams['ALPHA_LEFT_ZC_PART_SHIFT'])
    zcs_cands_end_index = zcs[cands_zcs_ids[-1]].index + int((zcs_peaks_cands_end_index - zcs[cands_zcs_ids[-1]].index) * PParams['ALPHA_RIGHT_ZC_PART_SHIFT'])
    zcs_peaks_cands_window = zcs_cands_end_index - zcs_cands_begin_index
    begin_part = float(PParams['ALPHA_PEAK_ADAPT_BEGIN_PART'])
    end_part = 1.0 - begin_part
    zcs_peaks_candidates_point = zcs_cands_begin_index + zcs_peaks_cands_window * begin_part

    peak_zc_id = 0
    peak_zc_mm_amplitude = 0.0

    for cand_zc_id in cands_zcs_ids:

        shift_percentage = float(zcs[cand_zc_id].index - zcs_peaks_candidates_point)
        if shift_percentage < 0.0:
            shift_percentage = abs(shift_percentage) / (zcs_peaks_cands_window * begin_part)
        else:
            shift_percentage = abs(shift_percentage) / (zcs_peaks_cands_window * end_part)

        amplitude_part = 1.0 - pow(shift_percentage, float(PParams['ALPHA_PEAK_ADAPT_POW'])) * float(PParams['ALPHA_PEAK_ADAPT_AMPL'])

        if zcs[cand_zc_id].s_ampl * amplitude_part >= peak_zc_mm_amplitude:
            peak_zc_id = cand_zc_id
            peak_zc_mm_amplitude = zcs[cand_zc_id].s_ampl * amplitude_part

    return peak_zc_id



