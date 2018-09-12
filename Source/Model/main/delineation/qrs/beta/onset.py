"""
Алгорим поиска начала QRS.

Входные параметры:
    ecg_lead - экземпляр класса отведения сигнала ЭКГ.
    delineation - экземпляр класса, содержащего информацию о текущем сегментированном комплексе.
    qrs_zc_id - индекс пересечения нуля детализирующими вейвлет-коэффициентами для текущего комплекса QRS.
    qrs_zcs - список пересечений нуля детализирующими вейвлет-коэффициентами.
    qrs_zc - пересечение нуля детализирующими вейвлет-коэффициентами для текущего комплекса QRS.
    mms - список экстремумов детализирующих вейвлет-коэффициентов.
    onset_mm_id - индекс экстремума, с которого начинается поиск начала QRS.
"""

from Source.Model.main.delineation.qrs.alpha.alpha import *
from Source.Model.main.delineation.qrs.routines import *
from Source.Model.main.delineation.wave_delineation import *
from Source.Model.main.threshold_crossings.routines import *
from Source.Model.main.modulus_maxima.routines import *


def define_qrs_onset_index(ecg_lead, delineation, qrs_zc):

    wdc_scale_id = get_qrs_wdc_scale_id(ecg_lead)
    wdc = ecg_lead.wdc[wdc_scale_id]
    rate = ecg_lead.rate
    window = int(float(QRSParams['BETA_ONSET_WINDOW']) * rate)
    mms = ecg_lead.mms[wdc_scale_id]

    zc = qrs_zc
    onset_mms = get_qrs_onset_mms(ecg_lead, zc)

    onset_mm_id = get_qrs_onset_mm_id(ecg_lead, zc, onset_mms, 0)
    complex_mm_id = get_complex_mm_id(ecg_lead, zc, onset_mms, onset_mm_id)

    if onset_mm_id != complex_mm_id:
        onset_mm_id = get_qrs_onset_mm_id(ecg_lead, zc, onset_mms, complex_mm_id)

    threshold = onset_mms[onset_mm_id].value * float(QRSParams['BETA_ONSET_THRESHOLD'])

    first_mm = onset_mms[onset_mm_id]
    next_mm = mms[first_mm.id - 1]

    if not next_mm.correctness:

        candidate_mm = mms[next_mm.id - 1]

        if abs(candidate_mm.value) > float(QRSParams['BETA_ONSET_MM_HIGH_LIM']) * abs(first_mm.value) \
                and abs(first_mm.index - candidate_mm.index) < int(float(QRSParams['BETA_ONSET_MM_WINDOW']) * rate):
            first_mm = candidate_mm
            next_mm = mms[first_mm.id - 1]
        else:
            onset_index_candidate_1 = next_mm.index
            onset_index_candidate_2 = find_left_thc_index(wdc, first_mm.index, zc.g_l_mm.index - window, threshold)
            onset_index = max(onset_index_candidate_1, onset_index_candidate_2)
            delineation.onset_index = onset_index
            return

    right_zc_index = find_right_thc_index(wdc, first_mm.index, zc.index, 0.0)
    left_zc_index = find_left_thc_index(wdc, first_mm.index, next_mm.index, 0.0)

    # Compromise
    compromise_window = int(float(QRSParams['BETA_ONSET_COMPROMISE_WINDOW']) * rate)
    compromise_mm_lim = float(QRSParams['BETA_ONSET_COMPROMISE_MM_LIM']) * min(abs(zc.g_l_mm.value), abs(zc.g_r_mm.value))
    if (right_zc_index - left_zc_index) > compromise_window \
            and abs(first_mm.value) < compromise_mm_lim:
        onset_index = first_mm.index
    else:
        onset_index = find_left_thc_index(wdc, first_mm.index, next_mm.index, threshold)

    delineation.onset_index = onset_index


def get_qrs_onset_mms(ecg_lead, qrs_zc):
    wdc_scale_id = get_qrs_wdc_scale_id(ecg_lead)
    rate = ecg_lead.rate
    window = int(float(QRSParams['BETA_ONSET_WINDOW']) * rate)
    mms = ecg_lead.mms[wdc_scale_id]

    onset_mms = [mms[qrs_zc.g_l_mm.id]]
    mm_id = qrs_zc.g_l_mm.id - 1
    while mm_id > 0 and qrs_zc.g_l_mm.index - mms[mm_id].index <= window:
        onset_mms.append(mms[mm_id])
        mm_id -= 1

    return onset_mms


def get_qrs_onset_mm_id(ecg_lead, qrs_zc, mms, onset_mm_id):
    rate = ecg_lead.rate
    window = int(float(QRSParams['BETA_ONSET_WINDOW']) * rate)

    mm_val = max(abs(qrs_zc.g_l_mm.value), abs(qrs_zc.g_r_mm.value)) * float(QRSParams['BETA_ONSET_MM_LOW_LIM'])

    start_index = qrs_zc.g_l_mm.index
    qrs_onset_mm_id = onset_mm_id
    if onset_mm_id + 1 < len(mms):
        for mm_id in range(onset_mm_id + 1, len(mms)):
            if mms[mm_id].correctness:
                shift_percentage = float(start_index - mms[mm_id].index) / float(window)
                amplitude_part = 1.0 - pow(shift_percentage, float(QRSParams['BETA_ONSET_AMPL_DECR_POW'])) * float(QRSParams['BETA_ONSET_AMPL_DECR_VAL'])

                if mm_val < abs(mms[mm_id].value) * amplitude_part:
                    qrs_onset_mm_id = mm_id
                else:
                    break

    return qrs_onset_mm_id


def get_complex_mm_id(ecg_lead, qrs_zc, mms, onset_mm_id):
    mm_val = max(abs(qrs_zc.g_l_mm.value), abs(qrs_zc.g_r_mm.value)) * float(QRSParams['BETA_ONSET_MM_LOW_LIM'])

    if onset_mm_id != len(mms) - 1:

        begin_mm_id = onset_mm_id + 1
        candidate_mm_id = onset_mm_id
        for mm_id in range(begin_mm_id, len(mms)):
            if abs(mms[mm_id].value) > float(QRSParams['BETA_COMPLEX_ZC_AMPL']) * abs(qrs_zc.g_ampl) \
                    or abs(mms[mm_id].value) > float(QRSParams['BETA_COMPLEX_MM_VAL']) * abs(qrs_zc.g_l_mm.value) \
                    or abs(mms[mm_id].value) > float(QRSParams['BETA_COMPLEX_MM_VAL']) * abs(qrs_zc.g_r_mm.value):
                candidate_mm_id = mm_id
                break

        if candidate_mm_id > onset_mm_id:
            is_new_candidate_correct = True
            if candidate_mm_id > begin_mm_id:
                for temp_mm_id in range(begin_mm_id, candidate_mm_id):
                    if abs(mms[temp_mm_id].value) > mm_val:
                        is_new_candidate_correct = False
                        break

            if is_new_candidate_correct:
                onset_mm_id = candidate_mm_id

    return onset_mm_id

