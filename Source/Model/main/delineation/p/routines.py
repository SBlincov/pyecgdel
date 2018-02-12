"""
Вспомогательные функции для алгоритма сегментации P.

Входные параметры:
    ecg_lead - экземпляр класса отведения сигнала ЭКГ.
    qrs_id - индекс текущего комплекса QRS.
"""

from Source.Model.main.params.p import *
from Source.Model.main.modulus_maxima.routines import *
from Source.Model.main.threshold_crossings.routines import *


class InvalidPProcessing(Exception):
    pass


def get_p_wdc_scale_id(ecg_lead):

    num_wdc_scales = len(ecg_lead.wdc)

    wdc_scale_id = int(PParams['WDC_SCALE_ID'])

    if wdc_scale_id > num_wdc_scales - 1:
        raise InvalidPProcessing('Wrong wdc scale id for p')

    return wdc_scale_id


def get_window(ecg_lead, qrs_id):

    sampling_rate = ecg_lead.sampling_rate

    cur_qrs_dels_seq = ecg_lead.cur_qrs_dels_seq

    qrs_gap = cur_qrs_dels_seq[qrs_id].onset_index - cur_qrs_dels_seq[qrs_id - 1].offset_index

    window_candidate_1 = int(qrs_gap * float(PParams['BEGIN_QRS_GAP_PROPORTION']))
    window_candidate_2 = int(sampling_rate * float(PParams['ZCS_SEARCHING_WINDOW']))

    window = min(window_candidate_1, window_candidate_2)

    cur_t_dels_seq = ecg_lead.cur_t_dels_seq

    if cur_t_dels_seq:

        corr_t_id = min(qrs_id - 1, len(cur_t_dels_seq) - 1)

        left_diff = cur_qrs_dels_seq[qrs_id].onset_index - cur_t_dels_seq[corr_t_id].offset_index

        while left_diff < 0 and corr_t_id > 0:
            corr_t_id -= 1
            left_diff = cur_qrs_dels_seq[qrs_id].onset_index - cur_t_dels_seq[corr_t_id].offset_index

        if left_diff > 0:
            window_candidate_3 = left_diff
            window = min(window, window_candidate_3)

    return window


def get_p_begin_index(ecg_lead, qrs_id):

    cur_qrs_dels_seq = ecg_lead.cur_qrs_dels_seq

    window = get_window(ecg_lead, qrs_id)
    begin_index = cur_qrs_dels_seq[qrs_id].onset_index - window

    return begin_index


def get_p_end_index(ecg_lead, qrs_id):

    cur_qrs_dels_seq = ecg_lead.cur_qrs_dels_seq
    wdc_scale_id = get_p_wdc_scale_id(ecg_lead)
    wdc = ecg_lead.wdc[wdc_scale_id]

    window = get_window(ecg_lead, qrs_id)
    begin_index = cur_qrs_dels_seq[qrs_id].onset_index - window
    tmp_mm = find_left_mm(cur_qrs_dels_seq[qrs_id].onset_index, wdc)
    end_index_candidate_1 = tmp_mm.index
    end_index_candidate_2 = find_left_thc_index(wdc, cur_qrs_dels_seq[qrs_id].onset_index, begin_index, 0.0)
    end_index = max(end_index_candidate_1, end_index_candidate_2 - 1)

    return end_index

