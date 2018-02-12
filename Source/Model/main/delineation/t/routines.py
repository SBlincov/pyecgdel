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

    wdc_scale_id = int(TParams['WDC_SCALE_ID'])

    if wdc_scale_id > num_wdc_scales - 1:
        raise InvalidTProcessing('Wrong wdc scale id for t')

    return wdc_scale_id


def get_window(ecg_lead, qrs_id):

    cur_qrs_dels_seq = ecg_lead.cur_qrs_dels_seq

    qrs_gap = cur_qrs_dels_seq[qrs_id].peak_index - cur_qrs_dels_seq[qrs_id - 1].peak_index

    window = qrs_gap * float(TParams['END_QRS_GAP_PROPORTION'])

    return window


def get_t_begin_index(ecg_lead, qrs_id):

    sampling_rate = ecg_lead.sampling_rate
    cur_qrs_dels_seq = ecg_lead.cur_qrs_dels_seq

    shift = int(float(TParams['BEGIN_SHIFT']) * sampling_rate)

    begin_index = cur_qrs_dels_seq[qrs_id - 1].offset_index + shift

    return begin_index


def get_t_end_index(ecg_lead, qrs_id):

    cur_qrs_dels_seq = ecg_lead.cur_qrs_dels_seq

    window = get_window(ecg_lead, qrs_id)

    end_index = int(cur_qrs_dels_seq[qrs_id - 1].offset_index + window)

    return end_index
