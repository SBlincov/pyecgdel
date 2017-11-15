import numpy as np
from Source.Model.main.params.qrs import QRSParams

def get_com_matrix(del_data, all_leads_data):

    num_total = len(all_leads_data.borders_counts)
    on_all_avg = []
    off_all_avg = []

    for complex_id in range(0, num_total):
        on_all_avg.append(all_leads_data.ons_sum[complex_id] / all_leads_data.borders_counts[complex_id])
        off_all_avg.append(all_leads_data.offs_sum[complex_id] / all_leads_data.borders_counts[complex_id])

    corr_mtx = []
    corr_lead = [-1] * num_total

    for lead_id in range(0, del_data.num_leads):

        ons_lead = del_data.ons[lead_id]
        offs_lead = del_data.offs[lead_id]

        for del_id in range(0, del_data.len_of_dels[lead_id]):

            if [lead_id, del_id] not in all_leads_data.del_candidates:

                on_diffs = []
                off_diffs = []

                for complex_id in range(0, num_total):
                    on_diffs.append(ons_lead[del_id] - on_all_avg[complex_id])
                    off_diffs.append(offs_lead[del_id] - off_all_avg[complex_id])

                on_argmin = np.argmin(np.absolute(np.asarray(on_diffs)))
                if on_argmin.size > 1:
                    on_argmin = on_argmin[0]
                on_min = on_diffs[on_argmin]

                off_argmin = np.argmin(np.absolute(np.asarray(off_diffs)))
                if off_argmin.size > 1:
                    off_argmin = off_argmin[0]
                off_min = off_diffs[off_argmin]

                # Additional checking:
                #   If global closest onset and offset correspond to the neighbour (not the same) complexes, we check:
                #       What provides smaller difference?
                if abs(on_argmin - off_argmin) == 1:

                    on_diff_own = on_diffs[on_argmin]
                    on_diff_der = on_diffs[off_argmin]

                    off_diff_own = off_diffs[off_argmin]
                    off_diff_der = off_diffs[on_argmin]

                    total_min = min([abs(on_diff_own), abs(on_diff_der), abs(off_diff_own), abs(off_diff_der)])

                    if total_min == abs(on_diff_own) or total_min == abs(off_diff_der):

                        off_argmin = on_argmin
                        off_min = off_diffs[off_argmin]

                    else:

                        on_argmin = off_argmin
                        on_min = on_diffs[on_argmin]

                if on_argmin == off_argmin:
                    argmin = on_argmin
                    corr_lead[argmin] = del_id

        corr_mtx.append(corr_lead)
        corr_lead = [-1] * num_total

    return corr_mtx
