from Source.Model.main.delineation.qrs.alpha.first import *
from Source.Model.main.delineation.qrs.alpha.second import *


def get_qrs_zcs_ids(ecg_lead, wdc_scale_id, aux_wdc_scale_id, qrs_zcs):

    candidates_zcs_ids = get_candidates_qrs_zcs_ids(ecg_lead, qrs_zcs)
    candidates_zcs_ids = get_confirmed_qrs_zcs_ids(ecg_lead, wdc_scale_id, candidates_zcs_ids, qrs_zcs)
    zcs_ids = get_confirmed_qrs_zcs_ids(ecg_lead, aux_wdc_scale_id, candidates_zcs_ids, qrs_zcs)

    zcs_ids = zcs_ids[1:-1]

    return zcs_ids


