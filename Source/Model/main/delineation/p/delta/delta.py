from Source.Model.main.delineation.p.delta.matrix import *
from Source.Model.main.delineation.p.delta.addition import *
from Source.Model.main.delineation.p.delta.removal import *

def p_multi_lead_processing(leads):

    num_leads = len(leads)

    del_data = DelData(leads)

    all_leads_data = AllLeadsData(del_data)

    delete_special(leads, del_data, all_leads_data)

    corr_mtx = get_com_matrix(del_data, all_leads_data)

    for g_id in range(0, len(all_leads_data.borders_counts)):

        p_count = 0
        mean_p_on = 0
        mean_p_off = 0

        for lead_id in range(0, num_leads):

            mtx_id = corr_mtx[lead_id][g_id]

            if mtx_id > -1:
                p_count += 1
                mean_p_on += del_data.ons[lead_id][mtx_id]
                mean_p_off += del_data.offs[lead_id][mtx_id]

        if p_count > 0:

            mean_p_on = int(mean_p_on / p_count)
            mean_p_off = int(mean_p_off / p_count)

            # Check for adding
            if p_count >= int(PParams['DELTA_MIN_P_FOUND'] * num_leads):

                add_complex(leads, corr_mtx, g_id, mean_p_on, mean_p_off)

            # Check for removing
            if p_count <= int(PParams['DELTA_MAX_P_LOST'] * num_leads):

                remove_complex(leads, corr_mtx, g_id)

    restore_morph_order(leads)

