from Source.Model.main.delineation.p.delta.data import *

def remove_complex(leads, corr_mtx, g_id):

    num_leads = len(leads)

    for lead_id in range(0, num_leads):

        # Delete only on existing leads
        if corr_mtx[lead_id][g_id] > -1:

            lead = leads[lead_id]

            # Morphology array stores target del, defined in del_id field of morphology
            for del_id in range(0, len(lead.p_dels)):
                if lead.p_morphs[del_id].del_id == corr_mtx[lead_id][g_id]:
                    lead.p_dels.pop(del_id)
                    lead.p_morphs.pop(del_id)
                    break


def delete_special(leads, del_data, all_leads_data):

    # Delete special cases from original leads
    if len(all_leads_data.del_candidates) > 0:
        for del_list in all_leads_data.del_candidates:
            leads[del_list[0]].p_dels.pop(del_list[1])
            leads[del_list[0]].p_morphs.pop(del_list[1])

        # Refresh DelData
        del_data = DelData(leads)