import numpy as np

from Source.Model.main.params.qrs import QRSParams


def get_confirmed_qrs_zcs_ids(ecg_lead, qrs_zcs, candidates_zcs_ids, wdc):

    rate = ecg_lead.rate

    qrs_len = qrs_zcs[candidates_zcs_ids[-1]].index - qrs_zcs[candidates_zcs_ids[0]].index

    if qrs_len <= int(2.0 * float(QRSParams['ALPHA_TRAINING_WINDOW']) * rate):
        training_window = qrs_len / rate * 0.5
        training_deltas_count = max(int(training_window * 0.5), 1)
    else:
        training_window = float(QRSParams['ALPHA_TRAINING_WINDOW'])
        training_deltas_count = int(QRSParams['ALPHA_BEATS_IN_TRAINING_WINDOW'])

    confirmed_zcs_ids = []

    window = int(rate * float(QRSParams['ALPHA_QRS_WINDOW']))

    deltas = []
    training_deltas = []

    for candidate_zc_id in candidates_zcs_ids:
        delta = get_delta(wdc, qrs_zcs[candidate_zc_id], window)
        deltas.append(delta)
        if qrs_zcs[candidate_zc_id].index <= rate * training_window + qrs_zcs[candidates_zcs_ids[0]].index:
            training_deltas.append(delta)

    correct_training_deltas = np.sort(training_deltas)[:-(training_deltas_count + 1):-1]

    if training_deltas_count > 1:
        epsilon = float(QRSParams['ALPHA_THRESHOLD']) * np.sum(correct_training_deltas[1:]) / (training_deltas_count - 1)
    else:
        epsilon = float(QRSParams['ALPHA_THRESHOLD']) * np.sum(correct_training_deltas) / training_deltas_count

    for i in range(len(training_deltas), len(deltas)):
        current_delta = deltas[i]
        if current_delta > epsilon:
            confirmed_zcs_ids.append(candidates_zcs_ids[i])
            correct_training_deltas = np.concatenate((correct_training_deltas[1:training_deltas_count], [current_delta]))
            epsilon = float(QRSParams['ALPHA_THRESHOLD']) * np.sum(correct_training_deltas) / training_deltas_count

    reversed_correct_training_deltas = []

    for i in range(min(training_deltas_count, len(confirmed_zcs_ids))):
        reversed_correct_training_deltas.append(get_delta(wdc, qrs_zcs[confirmed_zcs_ids[i]], window))

    epsilon = float(QRSParams['ALPHA_THRESHOLD']) * np.sum(reversed_correct_training_deltas) / training_deltas_count

    for i in range(len(training_deltas) - 1, -1, -1):
        current_delta = deltas[i]
        if current_delta > epsilon:
            confirmed_zcs_ids = [candidates_zcs_ids[i]] + confirmed_zcs_ids
            reversed_correct_training_deltas = np.concatenate(([current_delta], reversed_correct_training_deltas[0:training_deltas_count - 1]))
            epsilon = float(QRSParams['ALPHA_THRESHOLD']) * np.sum(reversed_correct_training_deltas) / training_deltas_count

    return confirmed_zcs_ids


def get_delta(wdc, qrs_zc, window):

    max_wdc = np.max(wdc[qrs_zc.index - np.min([window, qrs_zc.index]):qrs_zc.index + np.min([window, len(wdc) - qrs_zc.index])])
    min_wdc = np.min(wdc[qrs_zc.index - np.min([window, qrs_zc.index]):qrs_zc.index + np.min([window, len(wdc) - qrs_zc.index])])

    return max_wdc - min_wdc
