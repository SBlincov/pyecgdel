"""
Вспомогательные функции для алгоритма сегментации P.

Входные параметры:
    ecg_lead - экземпляр класса отведения сигнала ЭКГ.
    qrs_id - индекс текущего комплекса QRS.
"""

from Source.Model.main.params.p import PParams
from Source.Model.main.modulus_maxima.routines import find_left_mm, find_right_mm
from Source.Model.main.threshold_crossings.routines import find_left_thc_index, find_right_thc_index


class InvalidPProcessing(Exception):
    pass


def get_p_wdc_scale_id(ecg_lead):

    """
        Define WDC scale id for P delineation
        :param ecg_lead: certain ECG lead
        :return wdc_scale_id: WDC scale id for P delineation
    """

    num_wdc_scales = len(ecg_lead.wdc)

    wdc_scale_id = int(PParams['WDC_SCALE_ID'])

    if wdc_scale_id > num_wdc_scales - 1:
        raise InvalidPProcessing('Wrong wdc scale id for p')

    return wdc_scale_id


def get_window(ecg_lead, qrs_id):

    """
        Define searching window for P delineation
        :param ecg_lead: certain ECG lead
        :param qrs_id: id of QRS, to the left of which we delineate P
        :return window: window of P delineation
    """

    rate = ecg_lead.rate

    qrs_dels = ecg_lead.qrs_dels

    qrs_gap = qrs_dels[qrs_id].onset_index - qrs_dels[qrs_id - 1].offset_index

    window_candidate_1 = int(qrs_gap * float(PParams['ALPHA_ZCS_QRS_GAP']))
    window_candidate_2 = int(rate * float(PParams['ALPHA_ZCS_WINDOW']))

    window = min(window_candidate_1, window_candidate_2)

    t_dels = ecg_lead.t_dels

    if t_dels:

        corr_t_id = min(qrs_id - 1, len(t_dels) - 1)

        left_diff = qrs_dels[qrs_id].onset_index - t_dels[corr_t_id].offset_index

        while left_diff < 0 and corr_t_id > 0:
            corr_t_id -= 1
            left_diff = qrs_dels[qrs_id].onset_index - t_dels[corr_t_id].offset_index

        if left_diff > 0:
            window_candidate_3 = left_diff
            window = min(window, window_candidate_3)

    return window


def get_p_begin_index(ecg_lead, qrs_id):

    """
        Define begin index for P delineation
        :param ecg_lead: certain ECG lead
        :param qrs_id: id of QRS, to the left of which we delineate P
        :return begin_index: begin index for P delineation
    """

    qrs_dels = ecg_lead.qrs_dels

    window = get_window(ecg_lead, qrs_id)
    begin_index = qrs_dels[qrs_id].onset_index - window

    return begin_index


def get_p_end_index(ecg_lead, qrs_id):

    """
        Define end index for P delineation
        :param ecg_lead: certain ECG lead
        :param qrs_id: id of QRS, to the left of which we delineate P
        :return end_index: end index for P delineation
    """

    qrs_dels = ecg_lead.qrs_dels
    wdc_scale_id = get_p_wdc_scale_id(ecg_lead)
    wdc = ecg_lead.wdc[wdc_scale_id]

    window = get_window(ecg_lead, qrs_id)
    begin_index = qrs_dels[qrs_id].onset_index - window
    tmp_mm = find_left_mm(qrs_dels[qrs_id].onset_index, wdc)
    end_index_candidate_1 = tmp_mm.index
    end_index_candidate_2 = find_left_thc_index(wdc, qrs_dels[qrs_id].onset_index, begin_index, 0.0)
    end_index = max(end_index_candidate_1, end_index_candidate_2 - 1)

    return end_index

