"""
Алгорим поиска окончания QRS.

Входные параметры:
    ecg_lead - экземпляр класса отведения сигнала ЭКГ.
    delineation - экземпляр класса, содержащего информацию о текущем сегментированном комплексе.
    qrs_zc_id - индекс пересечения нуля детализирующими вейвлет-коэффициентами для текущего комплекса QRS.
    qrs_zcs - список пересечений нуля детализирующими вейвлет-коэффициентами.
    qrs_zc - пересечение нуля детализирующими вейвлет-коэффициентами для текущего комплекса QRS.
    mms - список экстремумов детализирующих вейвлет-коэффициентов.
    offset_mm_id - индекс экстремума, с которого начинается поиск окончания QRS.
"""

from Source.Model.main.delineation.qrs.alpha.alpha import *
from Source.Model.main.delineation.qrs.routines import *
from Source.Model.main.delineation.wave_delineation import *
from Source.Model.main.threshold_crossings.routines import *
from Source.Model.main.modulus_maxima.routines import *


def define_qrs_offset_index(ecg_lead, delineation, qrs_zc_id, qrs_zcs):

    wdc_scale_id = get_qrs_wdc_scale_id(ecg_lead)
    wdc = ecg_lead.wdc[wdc_scale_id]
    sampling_rate = ecg_lead.sampling_rate
    window = int(float(QRSParams['BETA_OFFSET_WINDOW']) * sampling_rate)

    zc = qrs_zcs[qrs_zc_id]
    mms = get_qrs_offset_mms(ecg_lead, zc)

    offset_mm_id = get_qrs_offset_mm_id(ecg_lead, zc, mms, 0)
    offset_mm_id_wide_morphology = get_complex_mm_id(ecg_lead, zc, mms, offset_mm_id)

    if offset_mm_id != offset_mm_id_wide_morphology:
        delineation.specification = WaveSpecification.flexure
        offset_mm_id = get_qrs_offset_mm_id(ecg_lead, zc, mms, offset_mm_id_wide_morphology)

    threshold = mms[offset_mm_id].value * float(QRSParams['BETA_OFFSET_THRESHOLD'])

    first_mm = mms[offset_mm_id]
    next_mm = find_right_mm(first_mm.index + 1, wdc)

    if not next_mm.correctness:
        if next_mm.index < zc.right_mm.index + window:
            offset_index_candidate_1 = next_mm.index
            offset_index_candidate_2 = find_right_thc_index(wdc, first_mm.index, zc.right_mm.index + window, threshold)
            offset_index = min(offset_index_candidate_1, offset_index_candidate_2)
        else:
            offset_index = find_right_thc_index(wdc, first_mm.index, zc.right_mm.index + window, threshold)
    else:
        offset_index = find_right_thc_index(wdc, first_mm.index, next_mm.index, threshold)

    delineation.offset_index = offset_index


def get_qrs_offset_mms(ecg_lead, qrs_zc):

    wdc_scale_id = get_qrs_wdc_scale_id(ecg_lead)
    wdc = ecg_lead.wdc[wdc_scale_id]
    sampling_rate = ecg_lead.sampling_rate
    window = int(float(QRSParams['BETA_OFFSET_WINDOW']) * sampling_rate)

    current_mm = ModulusMaxima(qrs_zc.right_mm.index, wdc)
    next_mm = find_right_mm(current_mm.index + 1, wdc)

    mms = [current_mm]

    while (next_mm.index - qrs_zc.right_mm.index) <= window \
            and next_mm.index < len(wdc) \
            and abs(current_mm.index - next_mm.index) > 0:
        current_mm = next_mm
        next_mm = find_right_mm(current_mm.index + 1, wdc)
        mms.append(current_mm)

    return mms


def get_qrs_offset_mm_id(ecg_lead, qrs_zc, mms, offset_mm_id):
    
    threshold = max(abs(qrs_zc.left_mm.value), abs(qrs_zc.right_mm.value)) * float(QRSParams['BETA_OFFSET_MM_LOW_LIM'])

    qrs_offset_mm_id = offset_mm_id

    if offset_mm_id + 1 < len(mms):
        for mm_id in range(offset_mm_id + 1, len(mms)):
            if mms[mm_id].correctness:
                if abs(mms[mm_id].value) > threshold:
                    qrs_offset_mm_id = mm_id
                else:
                    break

    return qrs_offset_mm_id


def get_complex_mm_id(ecg_lead, qrs_zc, mms, offset_mm_id):

    threshold = max(abs(qrs_zc.left_mm.value), abs(qrs_zc.right_mm.value)) * float(QRSParams['BETA_OFFSET_MM_LOW_LIM'])

    if offset_mm_id != len(mms) - 1:

        begin_mm_id = offset_mm_id + 1
        candidate_mm_id = offset_mm_id

        for mm_id in range(begin_mm_id, len(mms)):
            if abs(mms[mm_id].value) > float(QRSParams['BETA_COMPLEX_ZC_AMPL']) * abs(qrs_zc.mm_amplitude) \
                    or abs(mms[mm_id].value) > float(QRSParams['BETA_COMPLEX_MM_VAL']) * abs(qrs_zc.left_mm.value) \
                    or abs(mms[mm_id].value) > float(QRSParams['BETA_COMPLEX_MM_VAL']) * abs(qrs_zc.right_mm.value):
                candidate_mm_id = mm_id
                break

        if candidate_mm_id > offset_mm_id:

            is_new_candidate_correct = True

            if candidate_mm_id > begin_mm_id:

                for temp_mm_id in range(begin_mm_id, candidate_mm_id):
                    if abs(mms[temp_mm_id].value) > threshold:
                        is_new_candidate_correct = False
                        break

            if is_new_candidate_correct:
                offset_mm_id = candidate_mm_id

    return offset_mm_id

