from Source.Model.main.delineation.qrs.alpha.third import *
from Source.Model.main.delineation.qrs.routines import *
from Source.Model.main.zero_crossings.routines import *


def alpha_processing(ecg_lead, begin_index, end_index):
    wdc_scale_id = get_qrs_wdc_scale_id(ecg_lead)
    wdc_scale_id_aux = get_qrs_aux_wdc_scale_id(ecg_lead)
    wdc = ecg_lead.wdc[wdc_scale_id]
    wdc_aux = ecg_lead.wdc[wdc_scale_id_aux]

    # Main scale
    zcs = get_zcs_in_window(ecg_lead.wdc[wdc_scale_id], ecg_lead.zcs[wdc_scale_id], ecg_lead.ids_zcs[wdc_scale_id], begin_index, end_index)
    zcs_ids = get_candidates_qrs_zcs_ids(ecg_lead, zcs)
    zcs_ids = get_confirmed_qrs_zcs_ids(ecg_lead, zcs, zcs_ids, wdc)

    # Aux scale
    zcs_ids = get_confirmed_qrs_zcs_ids(ecg_lead, zcs, zcs_ids, wdc_aux)

    # Restore missed qrs
    zcs_ids = get_additional_qrs_zcs_ids(ecg_lead, zcs, zcs_ids, wdc, wdc_aux)

    # Exclude borders
    zcs_ids = zcs_ids[1:-1]

    qrs_zcs = []
    for zc_id in zcs_ids:
        qrs_zcs.append(zcs[zc_id])

    return qrs_zcs


