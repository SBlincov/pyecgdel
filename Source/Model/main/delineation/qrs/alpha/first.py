from Source.Model.main.params.qrs import QRSParams


def get_candidates_qrs_zcs_ids(ecg_lead, qrs_zcs):

    rate = ecg_lead.rate

    candidates_zcs_ids = []

    window = int(rate * float(QRSParams['ALPHA_MIN_BEAT']))

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
