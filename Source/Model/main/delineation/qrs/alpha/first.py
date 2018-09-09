from Source.Model.main.params.qrs import QRSParams


def get_candidates_qrs_zcs_ids(ecg_lead, zcs):
    rate = ecg_lead.rate
    window = int(rate * float(QRSParams['ALPHA_MIN_BEAT']))

    candidates_zcs_ids = []
    current_zc_id = 0
    next_zc_id = current_zc_id + 1
    while next_zc_id < len(zcs):
        while zcs[next_zc_id].index - zcs[current_zc_id].index < window and next_zc_id < len(zcs) - 1:
            if zcs[next_zc_id].g_ampl > zcs[current_zc_id].g_ampl:
                current_zc_id = next_zc_id
                next_zc_id = current_zc_id + 1
            else:
                next_zc_id += 1

        candidates_zcs_ids.append(current_zc_id)
        current_zc_id = next_zc_id
        next_zc_id = current_zc_id + 1

    return candidates_zcs_ids
