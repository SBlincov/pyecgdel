"""
Служебные функции, определяющие кандидатов на роль комплекса QRS.

Входные параметры:
    ecg_lead - экземпляр класса отведения сигнала ЭКГ.
    wdc_scale_id - первичная шкала вейвлет-коэффииентов, участвующих в алгоритме сегментации комплекса QRS.
    aux_wdc_scale_id - вспомогательная шкала вейвлет-коэффииентов, участвующих в алгоритме сегментации комплекса QRS.
    qrs_zcs - список пересечений нуля детализирующими вейвлет-коэффициентами.
    candidates_zcs_ids - индексы пересечений нуля детализирующими вейвлет-коэффициентами, являющиеся кандидатами на роль
    комплекса QRS.
    wdc - детализирующие вейвлет-коэффициенты.
    qrs_zc - пересечение нуля детализирующими вейвлет-коэффициентами для текущего комплекса QRS.
    window - область поиска вспомогательных характеристик.
"""

from Source.Model.main.ecg_lead.ecg_lead import *
from Source.Model.main.params.qrs import *
from Source.Model.main.zero_crossings.routines import *


def get_qrs_zcs_ids(ecg_lead, wdc_scale_id, aux_wdc_scale_id, qrs_zcs):

    candidates_zcs_ids = get_candidates_qrs_zcs_ids(ecg_lead, qrs_zcs)
    candidates_zcs_ids = get_confirmed_qrs_zcs_ids(ecg_lead, wdc_scale_id, candidates_zcs_ids, qrs_zcs)
    zcs_ids = get_confirmed_qrs_zcs_ids(ecg_lead, aux_wdc_scale_id, candidates_zcs_ids, qrs_zcs)

    zcs_ids = zcs_ids[1:-1]

    return zcs_ids


def get_candidates_qrs_zcs_ids(ecg_lead, qrs_zcs):

    sampling_rate = ecg_lead.sampling_rate

    candidates_zcs_ids = []

    window = int(sampling_rate * float(QRSParams['CANDIDATE_WINDOW_MIN_BEAT']))

    current_zc_id = 0

    next_zc_id = current_zc_id + 1

    while next_zc_id < len(qrs_zcs):

        while qrs_zcs[next_zc_id].index - qrs_zcs[current_zc_id].index < window and next_zc_id < len(qrs_zcs) - 1:

            if qrs_zcs[next_zc_id].mm_amplitude > qrs_zcs[current_zc_id].mm_amplitude:

                current_zc_id = next_zc_id
                next_zc_id = current_zc_id + 1

            else:
                next_zc_id += 1

        candidates_zcs_ids.append(current_zc_id)

        current_zc_id = next_zc_id
        next_zc_id = current_zc_id + 1

    return candidates_zcs_ids


def get_confirmed_qrs_zcs_ids(ecg_lead, wdc_scale_id, candidates_zcs_ids, qrs_zcs):

    sampling_rate = ecg_lead.sampling_rate
    wdc = ecg_lead.wdc[wdc_scale_id]

    if len(wdc) * sampling_rate <= 2.0 * float(QRSParams['CANDIDATE_WINDOW_TRAINING_PERIOD']):
        training_window = len(wdc) * sampling_rate * 0.5
        training_deltas_count = int(training_window * 0.5)
    else:
        training_window = float(QRSParams['CANDIDATE_WINDOW_TRAINING_PERIOD'])
        training_deltas_count = int(QRSParams['CANDIDATE_BEATS_COUNT_TRAINING_PERIOD'])

    confirmed_zcs_ids = []

    window = int(sampling_rate * float(QRSParams['CANDIDATE_WINDOW_DELTA']))

    deltas = []
    training_deltas = []

    for candidate_zc_id in candidates_zcs_ids:
        delta = get_delta(wdc, qrs_zcs[candidate_zc_id], window)
        deltas.append(delta)
        if qrs_zcs[candidate_zc_id].index <= sampling_rate * training_window:
            training_deltas.append(delta)

    correct_training_deltas = np.sort(training_deltas)[:-(training_deltas_count + 1):-1]

    if training_deltas_count > 1:
        epsilon = float(QRSParams['CANDIDATE_THRESHOLD_DELTA']) * np.sum(correct_training_deltas[1:]) / (training_deltas_count - 1)
    else:
        epsilon = float(QRSParams['CANDIDATE_THRESHOLD_DELTA']) * np.sum(correct_training_deltas) / training_deltas_count

    for i in range(len(training_deltas), len(deltas)):
        current_delta = deltas[i]
        if current_delta > epsilon:
            confirmed_zcs_ids.append(candidates_zcs_ids[i])
            correct_training_deltas = np.concatenate((correct_training_deltas[1:training_deltas_count], [current_delta]))
            epsilon = float(QRSParams['CANDIDATE_THRESHOLD_DELTA']) * np.sum(correct_training_deltas) / training_deltas_count

    reversed_correct_training_deltas = []

    for i in range(min(training_deltas_count, len(confirmed_zcs_ids))):
        reversed_correct_training_deltas.append(get_delta(wdc, qrs_zcs[confirmed_zcs_ids[i]], window))

    epsilon = float(QRSParams['CANDIDATE_THRESHOLD_DELTA']) * np.sum(reversed_correct_training_deltas) / training_deltas_count

    for i in range(len(training_deltas) - 1, -1, -1):
        current_delta = deltas[i]
        if current_delta > epsilon:
            confirmed_zcs_ids = [candidates_zcs_ids[i]] + confirmed_zcs_ids
            reversed_correct_training_deltas = np.concatenate(([current_delta], reversed_correct_training_deltas[0:training_deltas_count - 1]))
            epsilon = float(QRSParams['CANDIDATE_THRESHOLD_DELTA']) * np.sum(reversed_correct_training_deltas) / training_deltas_count

    return confirmed_zcs_ids


def get_delta(wdc, qrs_zc, window):

    max_wdc = np.max(wdc[qrs_zc.index - np.min([window, qrs_zc.index]):qrs_zc.index + np.min([window, len(wdc) - qrs_zc.index])])
    min_wdc = np.min(wdc[qrs_zc.index - np.min([window, qrs_zc.index]):qrs_zc.index + np.min([window, len(wdc) - qrs_zc.index])])

    return max_wdc - min_wdc


