import numpy as np
from Source.Model.main.delineation.p.delta.data import *

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

            on_diffs = []
            off_diffs = []

            for g_id in range(0, num_total):
                on_diffs.append(ons_lead[del_id] - on_all_avg[g_id])
                off_diffs.append(offs_lead[del_id] - off_all_avg[g_id])

            min_data = MinData(on_diffs, off_diffs)

            if min_data.on_argmin == min_data.off_argmin:
                argmin = min_data.on_argmin
                corr_lead[argmin] = del_id

        corr_mtx.append(corr_lead)

    return corr_mtx
