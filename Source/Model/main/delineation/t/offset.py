"""
Алгорим поиска окончания T.

Входные параметры:
    ecg_lead - экземпляр класса отведения сигнала ЭКГ.
    delineation - экземпляр класса, содержащего информацию о текущем сегментированном комплексе.
    zcs - список пересечений нуля детализирующими вейвлет-коэффициентами.
    right_peak_zc_id - индекс пересечения нуля, соответствующий правому пику комплекса (или единственному,
    если комплекс имеет стандартную морфологию).
    end_index - граница поиска.
"""

from Source.Model.main.params.t import *
from Source.Model.main.ecg_lead.ecg_lead import *
from Source.Model.main.modulus_maxima.routines import *
from Source.Model.main.delineation.t.delineation import *
from Source.Model.main.delineation.t.zcs import *


def define_t_offset_index(ecg_lead, delineation, zcs, right_peak_zc_id, end_index):

    wdc_scale_id = get_t_wdc_scale_id(ecg_lead)
    wdc = ecg_lead.wdc[wdc_scale_id]

    threshold = zcs[right_peak_zc_id].right_mm.value * float(TParams['ONSET_OFFSET_THRESHOLD_MM'])
    start_searching_offset_index = zcs[right_peak_zc_id].right_mm.index

    if start_searching_offset_index > end_index:
        raise InvalidWaveletProcessing('Error! t_offset out of borders')

    offset_index_candidate_1 = find_right_thc_index(wdc, start_searching_offset_index, end_index, threshold)
    offset_index_candidate_2 = offset_index_candidate_1

    mm_list = []
    candidate_mm = find_right_mm(zcs[right_peak_zc_id].right_mm.index + 1, wdc)

    while candidate_mm.index < end_index:
        mm_list.append(candidate_mm)
        candidate_mm = find_right_mm(candidate_mm.index + 1, wdc)

    if mm_list:
        for mm in mm_list:
            if not mm.correctness:
                offset_index_candidate_2 = mm.index

    delineation.offset_index = min(offset_index_candidate_1, offset_index_candidate_2)



