from Source.Model.main.delineation.qrs.alpha.first import *
from Source.Model.main.delineation.qrs.alpha.second import *
from Source.Model.main.delineation.qrs.routines import *
from Source.Model.main.zero_crossings.routines import *


def alpha_processing(ecg_lead, begin_index, end_index):

    sampling_rate = ecg_lead.sampling_rate
    wdc_scale_id = get_qrs_wdc_scale_id(ecg_lead)
    wdc_scale_id_aux = get_qrs_aux_wdc_scale_id(ecg_lead)
    wdc = ecg_lead.wdc[wdc_scale_id]
    wdc_aux = ecg_lead.wdc[wdc_scale_id_aux]

    # Main scale
    qrs_zcs = get_zcs_with_global_mms(wdc, begin_index, end_index)
    qrs_zcs_ids = get_candidates_qrs_zcs_ids(ecg_lead, qrs_zcs)
    qrs_zcs_ids = get_confirmed_qrs_zcs_ids(ecg_lead, qrs_zcs, qrs_zcs_ids, wdc)

    # Aux scale
    qrs_zcs_aux = get_zcs_with_global_mms(wdc_aux, begin_index, end_index)
    qrs_zcs_ids_aux = get_candidates_qrs_zcs_ids(ecg_lead, qrs_zcs_aux)
    qrs_zcs_ids_aux = get_confirmed_qrs_zcs_ids(ecg_lead, qrs_zcs_aux, qrs_zcs_ids_aux, wdc_aux)

    # Comparing
    comp_window = int(float(QRSParams['ALPHA_COMP_WINDOW']) * sampling_rate)
    aux_id = 0
    conf_qrs_zcs_ids = []
    for qrs_zcs_id in qrs_zcs_ids:
        qrs_zc = qrs_zcs[qrs_zcs_id]
        qrs_zc_aux = qrs_zcs_aux[qrs_zcs_ids_aux[aux_id]]

        curr_diff = qrs_zc_aux.index - qrs_zc.index
        next_diff = curr_diff
        while next_diff <= comp_window and aux_id < len(qrs_zcs_ids_aux) - 1:
            aux_id += 1
            qrs_zc_aux = qrs_zcs_aux[qrs_zcs_ids_aux[aux_id]]
            curr_diff = next_diff
            next_diff = qrs_zc_aux.index - qrs_zc.index

        if abs(curr_diff) <= comp_window:
            conf_qrs_zcs_ids.append(qrs_zcs_id)

    conf_qrs_zcs_ids = conf_qrs_zcs_ids[1:-1]

    return conf_qrs_zcs_ids


