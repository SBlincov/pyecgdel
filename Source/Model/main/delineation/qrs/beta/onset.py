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


def define_qrs_onset_index(ecg_lead, delineation, qrs_zc_id, qrs_zcs):

    wdc_scale_id = get_qrs_wdc_scale_id(ecg_lead)
    wdc = ecg_lead.wdc[wdc_scale_id]
    sampling_rate = ecg_lead.sampling_rate
    window = int(float(QRSParams['BETA_ONSET_WINDOW']) * sampling_rate)

    zc = qrs_zcs[qrs_zc_id]
    mms = get_qrs_onset_mms(ecg_lead, zc)

    onset_mm_id = get_qrs_onset_mm_id(ecg_lead, zc, mms, 0)
    complex_mm_id = get_complex_mm_id(ecg_lead, zc, mms, onset_mm_id)

    if onset_mm_id != complex_mm_id:
        delineation.specification = WaveSpecification.flexure
        onset_mm_id = get_qrs_onset_mm_id(ecg_lead, zc, mms, complex_mm_id)

    threshold = mms[onset_mm_id].value * float(QRSParams['BETA_ONSET_THRESHOLD'])

    first_mm = mms[onset_mm_id]
    next_mm = find_left_mm(first_mm.index - 1, wdc)

    if not next_mm.correctness:

        candidate_mm = find_left_mm(next_mm.index - 1, wdc)

        if abs(candidate_mm.value) > float(QRSParams['BETA_ONSET_MM_HIGH_LIM']) * abs(first_mm.value) \
                and abs(first_mm.index - candidate_mm.index) < int(float(QRSParams['BETA_ONSET_MM_WINDOW']) * sampling_rate):
            first_mm = candidate_mm
            next_mm = find_left_mm(first_mm.index - 1, wdc)
        else:
            onset_index_candidate_1 = next_mm.index
            onset_index_candidate_2 = find_left_thc_index(wdc, first_mm.index, zc.left_mm.index - window, threshold)
            onset_index = max(onset_index_candidate_1, onset_index_candidate_2)
            delineation.onset_index = onset_index
            return

    right_zc_index = find_right_thc_index(wdc, first_mm.index, zc.index, 0.0)
    left_zc_index = find_left_thc_index(wdc, first_mm.index, next_mm.index, 0.0)

    # Compromise
    if (right_zc_index - left_zc_index) > int(float(QRSParams['BETA_ONSET_COMPROMISE_WINDOW']) * sampling_rate) \
            and abs(first_mm.value) < float(QRSParams['BETA_ONSET_COMPROMISE_MM_LIM']) * min(abs(zc.left_mm.value), abs(zc.right_mm.value)):
        onset_index = first_mm.index
    else:
        onset_index = find_left_thc_index(wdc, first_mm.index, next_mm.index, threshold)

    delineation.onset_index = onset_index


def get_qrs_onset_mms(ecg_lead, qrs_zc):

    wdc_scale_id = get_qrs_wdc_scale_id(ecg_lead)
    wdc = ecg_lead.wdc[wdc_scale_id]
    sampling_rate = ecg_lead.sampling_rate
    window = int(float(QRSParams['BETA_ONSET_WINDOW']) * sampling_rate)

    current_mm = ModulusMaxima(qrs_zc.left_mm.index, wdc)
    next_mm = find_left_mm(current_mm.index - 1, wdc)

    mms = [current_mm]

    while (qrs_zc.left_mm.index - next_mm.index) <= window \
            and next_mm.index > 0 \
            and abs(current_mm.index - next_mm.index) > 0:
        current_mm = next_mm
        next_mm = find_left_mm(current_mm.index - 1, wdc)
        mms.append(current_mm)

    return mms


def get_qrs_onset_mm_id(ecg_lead, qrs_zc, mms, onset_mm_id):

    sampling_rate = ecg_lead.sampling_rate
    window = int(float(QRSParams['BETA_ONSET_WINDOW']) * sampling_rate)

    mm_val = max(abs(qrs_zc.left_mm.value), abs(qrs_zc.right_mm.value)) * float(QRSParams['BETA_ONSET_MM_LOW_LIM'])

    start_index = qrs_zc.left_mm.index

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

    mm_val = max(abs(qrs_zc.left_mm.value), abs(qrs_zc.right_mm.value)) * float(QRSParams['BETA_ONSET_MM_LOW_LIM'])

    if onset_mm_id != len(mms) - 1:

        begin_mm_id = onset_mm_id + 1
        candidate_mm_id = onset_mm_id

        for mm_id in range(begin_mm_id, len(mms)):

            if abs(mms[mm_id].value) > float(QRSParams['BETA_COMPLEX_ZC_AMPL']) * abs(qrs_zc.mm_amplitude) \
                    or abs(mms[mm_id].value) > float(QRSParams['BETA_COMPLEX_MM_VAL']) * abs(qrs_zc.left_mm.value) \
                    or abs(mms[mm_id].value) > float(QRSParams['BETA_COMPLEX_MM_VAL']) * abs(qrs_zc.right_mm.value):
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

