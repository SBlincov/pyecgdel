from Source.Model.main.delineation.qrs.delta.matrix import *
from Source.Model.main.delineation.qrs.delta.addition import *
from Source.Model.main.delineation.qrs.delta.removal import *

def multi_lead_processing(leads):

    num_leads = len(leads)

    del_data = DelData(leads)

    all_leads_data = AllLeadsData(del_data)

    delete_special(leads, del_data, all_leads_data)

    corr_mtx = get_com_matrix(del_data, all_leads_data)

    for g_id in range(0, len(all_leads_data.borders_counts)):

        qrs_count = 0
        mean_qrs_on = 0
        mean_qrs_off = 0

        for lead_id in range(0, num_leads):

            mtx_id = corr_mtx[lead_id][g_id]

            if mtx_id > -1:
                qrs_count += 1
                mean_qrs_on += del_data.ons[lead_id][mtx_id]
                mean_qrs_off += del_data.offs[lead_id][mtx_id]

        if qrs_count > 0:

            mean_qrs_on = int(mean_qrs_on / qrs_count)
            mean_qrs_off = int(mean_qrs_off / qrs_count)

            # Check for adding
            if qrs_count >= int(QRSParams['DELTA_MIN_QRS_FOUND'] * num_leads):

                add_complex(leads, corr_mtx, g_id, mean_qrs_on, mean_qrs_off)

            # Check for removing
            if qrs_count <= int(QRSParams['DELTA_MAX_QRS_LOST'] * num_leads):

                remove_complex(leads, corr_mtx, g_id)

    restore_morph_order(leads)


def restore_morph_order(leads):

    num_leads = len(leads)
    for lead_id in range(0, num_leads):
        lead = leads[lead_id]
        for morph_id in range(0, len(lead.qrs_morphs)):
            lead.qrs_morphs[morph_id].del_id = morph_id
