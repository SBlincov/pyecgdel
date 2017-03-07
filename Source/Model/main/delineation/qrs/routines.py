"""
Вспомогательные функции для алгоритма сегментации QRS.

Входные параметры:
    ecg_lead - экземпляр класса отведения сигнала ЭКГ.
"""

from Source.Model.main.params.qrs import *


class InvalidQRSProcessing(Exception):
    pass


def get_qrs_wdc_scale_id(ecg_lead):

    num_wdc_scales = len(ecg_lead.wdc)

    wdc_scale_id = int(QRSParams['QRS_WDC_SCALE_ID'])

    if wdc_scale_id > num_wdc_scales - 1:
        raise InvalidQRSProcessing('Wrong wdc scale id for qrs')

    return wdc_scale_id


def get_qrs_aux_wdc_scale_id(ecg_lead):

    num_wdc_scales = len(ecg_lead.wdc)

    wdc_scale_id_aux = int(QRSParams['QRS_WDC_SCALE_ID_AUX'])

    if wdc_scale_id_aux > num_wdc_scales - 1:
        raise InvalidQRSProcessing('Wrong wdc scale id aux for qrs')

    return wdc_scale_id_aux
