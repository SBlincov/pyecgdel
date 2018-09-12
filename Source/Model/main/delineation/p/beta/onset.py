"""
Алгорим поиска начала P.

Входные параметры:
    ecg_lead - экземпляр класса отведения сигнала ЭКГ.
    delineation - экземпляр класса, содержащего информацию о текущем сегментированном комплексе.
    zcs - список пересечений нуля детализирующими вейвлет-коэффициентами.
    left_peak_zc_id - индекс пересечения нуля, соответствующий левому пику комплекса (или единственному,
    если комплекс имеет стандартную морфологию).
    begin_index - граница поиска.
"""

from Source.Model.main.params.p_default import *
from Source.Model.main.ecg_lead.ecg_lead import *
from Source.Model.main.modulus_maxima.routines import *
from Source.Model.main.delineation.p.delineation import *
from Source.Model.main.delineation.p.zcs import *


def define_p_onset_index(ecg_lead, delineation, zcs, left_peak_zc_id, begin_index):
    wdc_scale_id = get_p_wdc_scale_id(ecg_lead)
    wdc = ecg_lead.wdc[wdc_scale_id]
    all_mms = ecg_lead.mms[wdc_scale_id]
    left_peak_zc = zcs[left_peak_zc_id]

    if left_peak_zc_id > 0:
        searching_onset_left_border_index = max(begin_index, zcs[left_peak_zc_id - 1].index)
    else:
        searching_onset_left_border_index = begin_index

    current_mm = all_mms[left_peak_zc.l_mms[0].id]
    onset_mm_candidate_coeff = abs(current_mm.value) * float(PParams['ALPHA_ONSET_MM'])

    mm_list = []
    while current_mm.index > searching_onset_left_border_index:
        mm_list.append(current_mm)
        current_mm = all_mms[current_mm.id - 1]

    if not mm_list:
        delineation.onset_index = searching_onset_left_border_index
        return

    correct_onset_mm_id = 0

    for onset_mm_id in range(1, len(mm_list)):
        if mm_list[onset_mm_id].correctness:
            if abs(mm_list[onset_mm_id].value) > onset_mm_candidate_coeff:
                correct_onset_mm_id = onset_mm_id

    mm_correct = mm_list[correct_onset_mm_id]
    onset_start_searching_index = mm_correct.index
    threshold = mm_correct.value * float(PParams['ALPHA_ONSET_OFFSET_THR'])

    onset_index_candidate_1 = find_left_thc_index(wdc, onset_start_searching_index, begin_index, threshold)
    onset_index_candidate_2 = all_mms[mm_correct.id - 1].index
    onset_index = max(onset_index_candidate_1, onset_index_candidate_2)

    delineation.onset_index = onset_index


