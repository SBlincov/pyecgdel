from Source.Model.main.delineation.qrs.delta.matrix import *
from Source.Model.main.delineation.qrs.delta.addition import *
from Source.Model.main.delineation.qrs.delta.removal import *

def qrs_multi_lead_processing(leads):

    num_leads = len(leads)

    del_data = DelData(leads)

    all_leads_data = AllLeadsData(del_data)

    delete_special(leads, del_data, all_leads_data)

    corr_mtx = get_com_matrix(del_data, all_leads_data)

    for g_id in range(0, len(all_leads_data.borders_counts)):

        qrs_count = 0
        qrs_ons = []
        qrs_peaks = []
        qrs_offs = []

        for lead_id in range(0, num_leads):

            mtx_id = corr_mtx[lead_id][g_id]

            if mtx_id > -1:
                qrs_count += 1
                qrs_ons.append(del_data.ons[lead_id][mtx_id])
                qrs_peaks.append(del_data.peaks[lead_id][mtx_id])
                qrs_offs.append(del_data.offs[lead_id][mtx_id])

        if qrs_count > 0:

            mean_qrs_on = np.mean(qrs_ons)
            mean_qrs_peak = np.mean(qrs_peaks)
            mean_qrs_off = np.mean(qrs_offs)

            std_qrs_on = np.std(qrs_ons)
            std_qrs_peak = np.std(qrs_peaks)
            std_qrs_off = np.std(qrs_offs)

            # Check for removing
            if qrs_count <= int(QRSParams['DELTA_MAX_QRS_LOST'] * num_leads):

                remove_complex(leads, corr_mtx, g_id)



            # Check for adding
            if qrs_count >= int(QRSParams['DELTA_MIN_QRS_FOUND'] * num_leads):

                add_complex(leads, corr_mtx, g_id, mean_qrs_on, mean_qrs_off)

    restore_morph_order(leads)


def restore_morph_order(leads):

    num_leads = len(leads)
    for lead_id in range(0, num_leads):
        lead = leads[lead_id]
        for morph_id in range(0, len(lead.qrs_morphs)):
            lead.qrs_morphs[morph_id].del_id = morph_id
