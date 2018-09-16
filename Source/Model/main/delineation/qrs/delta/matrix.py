import numpy as np
from Source.Model.main.delineation.qrs.delta.data import *
from Source.Model.main.search.closest_position import *


def get_com_matrix(del_data, all_leads_data):

    num_total = len(all_leads_data.borders_counts)
    on_all_avg = []
    off_all_avg = []

    # Define averaged values for each complex
    for g_id in range(0, num_total):
        on_all_avg.append(all_leads_data.ons_sum[g_id] / all_leads_data.borders_counts[g_id])
        off_all_avg.append(all_leads_data.offs_sum[g_id] / all_leads_data.borders_counts[g_id])

    # Matrix of correspondence:
    corr_mtx = []

    for lead_id in range(0, del_data.num_leads):

        corr_lead = [-1] * num_total

        ons_lead = del_data.ons[lead_id]
        offs_lead = del_data.offs[lead_id]

        for del_id in range(0, del_data.len_of_dels[lead_id]):

            on_argmin = get_closest(on_all_avg, ons_lead[del_id])
            off_argmin = get_closest(off_all_avg, offs_lead[del_id])

            # Additional checking:
            #   If global closest onset and offset correspond to the neighbour (not the same) complexes, we check:
            #       What provides smaller difference?
            if abs(on_argmin - off_argmin) == 1:
                on_diff_own = ons_lead[del_id] - on_all_avg[on_argmin]
                on_diff_der = ons_lead[del_id] - on_all_avg[off_argmin]

                off_diff_own = offs_lead[del_id] - off_all_avg[off_argmin]
                off_diff_der = offs_lead[del_id] - off_all_avg[on_argmin]

                total_min = min([abs(on_diff_own), abs(on_diff_der), abs(off_diff_own), abs(off_diff_der)])

                if total_min == abs(on_diff_own) or total_min == abs(off_diff_der):
                    off_argmin = on_argmin
                else:
                    on_argmin = off_argmin

            if on_argmin == off_argmin:
                argmin = on_argmin
                corr_lead[argmin] = del_id

        corr_mtx.append(corr_lead)

    return corr_mtx

def restore_morph_order(leads):
    num_leads = len(leads)
    for lead_id in range(0, num_leads):
        lead = leads[lead_id]
        for morph_id in range(0, len(lead.qrs_morphs)):
            lead.qrs_morphs[morph_id].del_id = morph_id

