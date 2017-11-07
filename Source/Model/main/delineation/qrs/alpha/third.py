from Source.Model.main.delineation.qrs.alpha.first import *
from Source.Model.main.delineation.qrs.alpha.second import *


def get_additional_qrs_zcs_ids(ecg_lead, zcs, zcs_ids, wdc, wdc_aux):
    zcs_diffs = []
    for zc_id in range(len(zcs_ids) - 1):
        zcs_diffs.append(zcs[zcs_ids[zc_id + 1]].index - zcs[zcs_ids[zc_id]].index)
    mean_zcs_diff = np.mean(zcs_diffs)

    for zc_id in range(len(zcs_ids) - 1):

        if (zcs[zcs_ids[zc_id + 1]].index - zcs[zcs_ids[zc_id]].index) > float(QRSParams['ALPHA_SKIP']) * mean_zcs_diff:

            zcs_ids_add = get_candidates_qrs_zcs_ids(ecg_lead, zcs[zcs_ids[zc_id]:zcs_ids[zc_id + 1]])

            for zc_id_add in range(len(zcs_ids_add)):
                zcs_ids_add[zc_id_add] = zcs_ids_add[zc_id_add] + zcs_ids[zc_id]

            if len(zcs_ids_add) > 0:
                begin_zc = zcs[zcs_ids_add[0]]
                end_zc = zcs[zcs_ids_add[-1]]

                zcs_ids_add = get_confirmed_qrs_zcs_ids(ecg_lead, zcs, zcs_ids_add, wdc)
                zcs_ids_add = get_confirmed_qrs_zcs_ids(ecg_lead, zcs, zcs_ids_add, wdc_aux)
                if zcs_ids_add:
                    zcs_ids = zcs_ids + zcs_ids_add

    zcs_ids = np.sort(zcs_ids)

    return zcs_ids
