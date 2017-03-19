"""
Функция поиска пересечения нуля для алгоритма сегментации P.

Входные параметры:
    ecg_lead - экземпляр класса отведения сигнала ЭКГ.
    qrs_id - индекс текущего комплекса QRS.
    window - окно поиска.
"""

from Source.Model.main.params.p_default import *
from Source.Model.main.ecg_lead.ecg_lead import *
from Source.Model.main.modulus_maxima.routines import *
from Source.Model.main.delineation.p.routines import *


def get_p_zcs(ecg_lead, qrs_id, window):

    wdc_scale_id = get_p_wdc_scale_id(ecg_lead)
    wdc = ecg_lead.wdc[wdc_scale_id]

    begin_index = get_p_begin_index(ecg_lead, qrs_id)
    end_index = get_p_end_index(ecg_lead, qrs_id)

    zcs = get_zcs_with_special_mms_for_p(wdc, begin_index, end_index, window)

    return zcs



