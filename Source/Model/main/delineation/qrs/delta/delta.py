from Source.Model.main.delineation.qrs.delta.matrix import *
from Source.Model.main.delineation.qrs.delta.addition import *
from Source.Model.main.delineation.qrs.delta.removal import *
from Source.Model.main.delineation.qrs.delta.shift import *
from Source.Model.main.zero_crossings.routines import *
from Source.Model.main.threshold_crossings.routines import *


def qrs_multi_lead_processing(leads):
    num_leads = len(leads)

    del_data = DelData(leads)

    all_leads_data = AllLeadsData(del_data)

    delete_special(leads, del_data, all_leads_data)

    corr_mtx = get_com_matrix(del_data, all_leads_data)

    stat_data = StatData(leads, all_leads_data, del_data, corr_mtx)

    shift_all(leads, del_data, all_leads_data, corr_mtx, stat_data)

    for g_id in range(0, len(all_leads_data.borders_counts)):

        qrs_count = stat_data.counts[g_id]
        qrs_ons = stat_data.ons[g_id]
        qrs_peaks = stat_data.peaks[g_id]
        qrs_offs = stat_data.offs[g_id]

        if qrs_count > 0:

            mean_qrs_on = int(np.mean(qrs_ons))
            mean_qrs_peak = int(np.mean(qrs_peaks))
            mean_qrs_off = int(np.mean(qrs_offs))

            # Check for removing
            if qrs_count <= int(QRSParams['DELTA_MAX_QRS_LOST'] * num_leads):
                remove_complex(leads, corr_mtx, g_id)

            # Check for adding
            if qrs_count >= int(QRSParams['DELTA_MIN_QRS_FOUND'] * num_leads):
                add_complex(leads, corr_mtx, g_id, mean_qrs_on, mean_qrs_off)

    restore_morph_order(leads)



