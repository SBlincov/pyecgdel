from Source.Model.main.delineation.qrs.delta.data import *
from Source.Model.main.delineation.qrs.delta.matrix import *


def remove_complex(leads, corr_mtx, g_id):

    num_leads = len(leads)

    for lead_id in range(0, num_leads):

        # Delete only on existing leads
        if corr_mtx[lead_id][g_id] > -1:

            lead = leads[lead_id]

            # Morphology array stores target del, defined in del_id field of morphology
            for del_id in range(0, len(lead.qrs_dels)):
                if lead.qrs_morphs[del_id].del_id == corr_mtx[lead_id][g_id]:
                    lead.qrs_dels.pop(del_id)
                    lead.qrs_morphs.pop(del_id)
                    break

def delete_nearest(leads):

    num_leads = len(leads)

    for lead_id in range(0, num_leads):

        peaks = []

        lead = leads[lead_id]

        neartest_dist = float(QRSParams['DELTA_NEAREST']) * lead.rate

        for del_id in range(0, len(lead.qrs_dels)):
            peaks.append(lead.qrs_dels[del_id].peak_index)

        peaks_diffs = np.diff(peaks)

        dels_indexes = []
        for diff_id in range(0, len(peaks_diffs)):
            if abs(peaks_diffs[diff_id]) < neartest_dist:
                dels_indexes.append(diff_id)

        for del_id in reversed(dels_indexes):
            lead.qrs_dels.pop(del_id)
            lead.qrs_morphs.pop(del_id)

