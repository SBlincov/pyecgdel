"""
Алгорим поиска начала T.

Входные параметры:
    ecg_lead - экземпляр класса отведения сигнала ЭКГ.
    delineation - экземпляр класса, содержащего информацию о текущем сегментированном комплексе.
    zcs - список пересечений нуля детализирующими вейвлет-коэффициентами.
    left_peak_zc_id - индекс пересечения нуля, соответствующий левому пику комплекса (или единственному,
    если комплекс имеет стандартную морфологию).
    begin_index - граница поиска.
"""

from Source.Model.main.params.t import *
from Source.Model.main.ecg_lead.ecg_lead import *
from Source.Model.main.modulus_maxima.routines import *
from Source.Model.main.delineation.t.delineation import *
from Source.Model.main.delineation.t.zcs import *


def define_t_onset_index(ecg_lead, delineation, zcs, left_peak_zc_id, begin_index):
    wdc_scale_id = get_t_wdc_scale_id(ecg_lead)
    wdc = ecg_lead.wdc[wdc_scale_id]
    all_mms = ecg_lead.mms[wdc_scale_id]

    threshold = zcs[left_peak_zc_id].s_l_mm.value * float(TParams['ALPHA_ONSET_OFFSET_MM'])
    start_searching_onset_index = zcs[left_peak_zc_id].s_l_mm.index

    if start_searching_onset_index < begin_index:
        start_searching_onset_index = zcs[left_peak_zc_id].l_l_mm.index

    onset_index_candidate_1 = find_left_thc_index(wdc, start_searching_onset_index, begin_index, threshold)
    onset_index_candidate_2 = onset_index_candidate_1

    mm_list = []
    candidate_mm = all_mms[zcs[left_peak_zc_id].s_l_mm.id - 1]

    while candidate_mm.index > begin_index:
        mm_list.append(candidate_mm)
        candidate_mm = all_mms[candidate_mm.id - 1]

    if mm_list:
        for mm in mm_list:
            if not mm.correctness:
                onset_index_candidate_2 = mm.index

    delineation.onset_index = max(onset_index_candidate_1, onset_index_candidate_2)


