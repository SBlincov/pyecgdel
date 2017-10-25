import numpy as np
from Source.Model.main.params.qrs import QRSParams


def get_com_matrix(leads, borders_counts, ons_sum, offs_sum, del_candidates):

    num_leads = len(leads)

    ons = []
    offs = []
    len_of_dels = []
    mean_qrs = []

    for lead_id in range(0, num_leads):

        lead = leads[lead_id]
        dels = lead.qrs_dels

        len_of_dels.append(len(dels))

        ons_lead = []
        offs_lead = []
        mean_qrs_curr = 0.0
        for del_id in range(0, len_of_dels[lead_id]):
            on_index_curr = dels[del_id].onset_index
            off_index_curr = dels[del_id].offset_index
            ons_lead.append(on_index_curr)
            offs_lead.append(off_index_curr)
            mean_qrs_curr += (off_index_curr - on_index_curr)

        if len(dels) > 0:
            mean_qrs_curr /= len(dels)

        ons.append(ons_lead)
        offs.append(offs_lead)
        mean_qrs.append(mean_qrs_curr)

    # Computing global mean QRS length
    mean_qrs_global = np.mean(np.asarray(mean_qrs))

    diff_corr = mean_qrs_global * float(QRSParams['DELTA_MEAN_QRS_DIFF_CORR'])

    num_total = len(borders_counts)
    on_all_avg = []
    off_all_avg = []

    for complex_id in range(0, num_total):
        on_all_avg.append(ons_sum[complex_id] / borders_counts[complex_id])
        off_all_avg.append(offs_sum[complex_id] / borders_counts[complex_id])

    corr_mtx = []
    corr_lead = [-1] * num_total

    for lead_id in range(0, num_leads):

        ons_lead = ons[lead_id]
        offs_lead = offs[lead_id]

        for del_id in range(0, len_of_dels[lead_id]):

            if [lead_id, del_id] not in del_candidates:

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

                # Additional checking of argmins
                if abs(on_argmin - off_argmin) == 1:

                    on_diff_own = on_diffs[on_argmin]
                    on_diff_der = on_diffs[off_argmin]

                    off_diff_own = off_diffs[off_argmin]
                    off_diff_der = off_diffs[on_argmin]

                    on_diff_diff_abs = abs(abs(on_diff_own) - abs(on_diff_der))
                    off_diff_diff_abs = abs(abs(off_diff_own) - abs(off_diff_der))

                    if (on_diff_diff_abs < off_diff_diff_abs) and (on_diff_diff_abs < diff_corr):

                        on_argmin = off_argmin
                        on_min = on_diffs[on_argmin]

                    elif (off_diff_diff_abs < on_diff_diff_abs) and (off_diff_diff_abs < diff_corr):

                        off_argmin = on_argmin
                        off_min = off_diffs[off_argmin]

                    else:

                        total_min = min([abs(on_diff_own), abs(on_diff_der), abs(off_diff_own), abs(off_diff_der)])

                        if total_min == abs(on_diff_own) or total_min == abs(off_diff_own):

                            on_argmin = off_argmin
                            on_min = on_diffs[on_argmin]

                        else:

                            off_argmin = on_argmin
                            off_min = off_diffs[off_argmin]

                if on_argmin == off_argmin:
                    argmin = on_argmin
                    corr_lead[argmin] = del_id

        corr_mtx.append(corr_lead)
        corr_lead = [-1] * num_total

    return corr_mtx
