"""
Функция поиска пересечения нуля для алгоритма сегментации T.

Входные параметры:
    ecg_lead - экземпляр класса отведения сигнала ЭКГ.
    qrs_id - индекс текущего комплекса QRS.
    window - окно поиска.
"""

from Source.Model.main.ecg_lead.ecg_lead import *
from Source.Model.main.delineation.t.routines import *


def get_t_zcs(ecg_lead, qrs_id, window):

    wdc_scale_id = get_t_wdc_scale_id(ecg_lead)

    begin_index = get_t_begin_index(ecg_lead, qrs_id)
    end_index = get_t_end_index(ecg_lead, qrs_id)

    zcs = get_zcs_in_window(ecg_lead.wdc[wdc_scale_id], ecg_lead.zcs[wdc_scale_id], ecg_lead.ids_zcs[wdc_scale_id], begin_index, end_index)
    if len(zcs) > 0:
        if len(zcs) == 1:
            zcs[0].special(ecg_lead.wdc[wdc_scale_id], max(begin_index, zcs[0].index - window), min(end_index, zcs[0].index + window))
        elif len(zcs) == 2:
            zcs[0].special(ecg_lead.wdc[wdc_scale_id], max(begin_index, zcs[0].index - window), min(zcs[1].index, zcs[0].index + window))
            zcs[-1].special(ecg_lead.wdc[wdc_scale_id], max(zcs[-2].index, zcs[-1].index - window), min(end_index, zcs[-1].index + window))
        else:
            zcs[0].special(ecg_lead.wdc[wdc_scale_id], max(begin_index, zcs[0].index - window), min(zcs[1].index, zcs[0].index + window))

            for zc_id in range (1, len(zcs) - 1):
                zcs[zc_id].special(ecg_lead.wdc[wdc_scale_id], max(zcs[zc_id - 1].index, zcs[zc_id].index - window), min(zcs[zc_id + 1].index, zcs[zc_id].index + window))

            zcs[-1].special(ecg_lead.wdc[wdc_scale_id], max(zcs[-2].index, zcs[-1].index - window), min(end_index, zcs[-1].index + window))

    return zcs

