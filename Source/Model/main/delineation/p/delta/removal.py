from Source.Model.main.delineation.p.delta.data import *
from Source.Model.main.delineation.p.delta.matrix import *

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


    if len(all_leads_data.del_candidates) > 0:

        for lead_id in all_leads_data.del_candidates:

            tmp_p_dels = [leads[lead_id].p_dels[x] for x in range(0, len(leads[lead_id].p_dels)) if x not in all_leads_data.del_candidates[lead_id]]
            tmp_p_morphs = [leads[lead_id].p_morphs[x] for x in range(0, len(leads[lead_id].p_morphs)) if x not in all_leads_data.del_candidates[lead_id]]

            leads[lead_id].p_dels = tmp_p_dels
            leads[lead_id].p_morphs = tmp_p_morphs

        # Refresh DelData
        del_data = DelData(leads)
        del_data.process(leads)
        restore_morph_order(leads)
