"""
Вспомогательные функции для алгоритма сегментации T.

Входные параметры:
    ecg_lead - экземпляр класса отведения сигнала ЭКГ.
    qrs_id - индекс текущего комплекса QRS.
"""

from Source.Model.main.params.t import *


class InvalidTProcessing(Exception):
    pass


def get_t_wdc_scale_id(ecg_lead):
    num_wdc_scales = len(ecg_lead.wdc)

    wdc_scale_id = int(TParams['T_WDC_SCALE_ID'])

    if wdc_scale_id > num_wdc_scales - 1:
        raise InvalidTProcessing('Wrong wdc scale id for t')

    return wdc_scale_id


def get_window(ecg_lead, qrs_id):

    cur_qrs_dels_seq = ecg_lead.cur_qrs_dels_seq
    cur_p_dels_seq = ecg_lead.cur_p_dels_seq

    rr = cur_qrs_dels_seq[qrs_id].peak_index - cur_qrs_dels_seq[qrs_id - 1].peak_index

    window = rr * float(TParams['END_PROPORTION'])

    if cur_p_dels_seq:

        corr_p_id = min(qrs_id - 1, len(cur_p_dels_seq) - 1)

        left_diff = cur_qrs_dels_seq[qrs_id].peak_index - cur_p_dels_seq[corr_p_id].peak_index

        while left_diff < 0 and corr_p_id > 0:
            corr_p_id -= 1
            left_diff = cur_qrs_dels_seq[qrs_id].peak_index - cur_p_dels_seq[corr_p_id].peak_index

        for p_id in range(corr_p_id, len(cur_p_dels_seq)):
            if cur_p_dels_seq[p_id].offset_index < cur_qrs_dels_seq[qrs_id].onset_index:
                corr_p_id = p_id
            else:
                break

        if cur_qrs_dels_seq[qrs_id].onset_index - cur_p_dels_seq[corr_p_id].offset_index < int(rr * float(TParams['P_CORR'])):
            window_candidate_1 = window
            window_candidate_2 = cur_p_dels_seq[corr_p_id].onset_index - cur_qrs_dels_seq[qrs_id - 1].offset_index
            window = min(window_candidate_1, window_candidate_2)

    return window


def get_t_begin_index(ecg_lead, qrs_id):

    sampling_rate = ecg_lead.sampling_rate
    cur_qrs_dels_seq = ecg_lead.cur_qrs_dels_seq

    begin_index = int(cur_qrs_dels_seq[qrs_id - 1].offset_index + float(TParams['START_SHIFT']) * sampling_rate)

    return begin_index


def get_t_end_index(ecg_lead, qrs_id):

    cur_qrs_dels_seq = ecg_lead.cur_qrs_dels_seq

    window = get_window(ecg_lead, qrs_id)
    end_index = int(cur_qrs_dels_seq[qrs_id - 1].offset_index + window)

    return end_index
