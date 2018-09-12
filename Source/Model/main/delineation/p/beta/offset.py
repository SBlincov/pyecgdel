"""
Алгорим поиска окончания P.

Входные параметры:
    ecg_lead - экземпляр класса отведения сигнала ЭКГ.
    delineation - экземпляр класса, содержащего информацию о текущем сегментированном комплексе.
    zcs - список пересечений нуля детализирующими вейвлет-коэффициентами.
    right_peak_zc_id - индекс пересечения нуля, соответствующий правому пику комплекса (или единственному,
    если комплекс имеет стандартную морфологию).
    end_index - граница поиска.
"""

from Source.Model.main.params.p_default import *
from Source.Model.main.ecg_lead.ecg_lead import *
from Source.Model.main.modulus_maxima.routines import *
from Source.Model.main.delineation.p.delineation import *
from Source.Model.main.delineation.p.zcs import *


def define_p_offset_index(ecg_lead, delineation, zcs, right_peak_zc_id, end_index):
    wdc_scale_id = get_p_wdc_scale_id(ecg_lead)
    wdc = ecg_lead.wdc[wdc_scale_id]
    all_mms = ecg_lead.mms[wdc_scale_id]
    right_peak_zc = zcs[right_peak_zc_id]


    if right_peak_zc_id < len(zcs) - 1:
        searching_offset_right_border_index = min(end_index, zcs[right_peak_zc_id + 1].index)
    else:
        searching_offset_right_border_index = end_index

    current_mm = all_mms[right_peak_zc.r_mms[0].id]
    offset_mm_candidate_coeff = abs(current_mm.value) * float(PParams['ALPHA_OFFSET_MM'])
    offset_mm_candidate_coeff_overflow = abs(current_mm.value) * float(PParams['ALPHA_OFFSET_MM_OVERFLOW'])

    mm_list = []
    while current_mm.index < searching_offset_right_border_index:
        mm_list.append(current_mm)
        current_mm = all_mms[current_mm.id + 1]

    if not mm_list:
        delineation.offset_index = searching_offset_right_border_index
        return

    correct_offset_mm_id = 0

    if delineation.specification is not WaveSpecification.biphasic:

        for offset_mm_id in range(1, len(mm_list)):
            if mm_list[offset_mm_id].correctness:
                if offset_mm_candidate_coeff < abs(mm_list[offset_mm_id].value) < offset_mm_candidate_coeff_overflow:
                    if mm_list[correct_offset_mm_id].value * mm_list[offset_mm_id].value > 0:
                        correct_offset_mm_id = offset_mm_id
                else:
                    break
            else:
                delineation.offset_index = mm_list[offset_mm_id].index
                return

    mm_correct = mm_list[correct_offset_mm_id]
    offset_start_searching_index = mm_correct.index
    threshold = mm_correct.value * float(PParams['ALPHA_ONSET_OFFSET_THR'])

    offset_index_candidate_1 = find_right_thc_index(wdc, offset_start_searching_index, end_index, threshold)
    offset_index_candidate_2 = all_mms[mm_correct.id + 1].index
    offset_index = min(offset_index_candidate_1, offset_index_candidate_2)

    delineation.offset_index = offset_index
