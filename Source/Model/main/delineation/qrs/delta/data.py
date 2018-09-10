import numpy as np
from Source.Model.main.params.qrs import QRSParams
import warnings

class DelData:

    def __init__(self, leads):

        num_leads = len(leads)

        ons = []
        peaks = []
        offs = []
        num_points = []
        len_of_dels = []
        mean_qrs = []

        # Considering all leads:
        #   Taking all onset, peak and offset indexes
        #   Saving number of dels for each lead
        #   Saving mean QRS length for each lead
        for lead_id in range(0, num_leads):

            lead = leads[lead_id]

            dels = lead.qrs_dels
            morphs = lead.qrs_morphs

            len_of_dels.append(len(dels))

            ons_lead = []
            peaks_lead = []
            offs_lead = []
            num_points_lead = []
            mean_qrs_curr = 0.0
            for del_id in range(0, len_of_dels[lead_id]):
                on_index_curr = dels[del_id].onset_index
                peak_index_curr = dels[del_id].peak_index
                off_index_curr = dels[del_id].offset_index
                num_points_curr = len(morphs[del_id].points)
                ons_lead.append(on_index_curr)
                peaks_lead.append(peak_index_curr)
                offs_lead.append(off_index_curr)
                num_points_lead.append(num_points_curr)
                mean_qrs_curr += (off_index_curr - on_index_curr)

            if len(dels) > 0:
                mean_qrs_curr /= len(dels)

            ons.append(ons_lead)
            peaks.append(peaks_lead)
            offs.append(offs_lead)
            num_points.append(num_points_lead)
            mean_qrs.append(mean_qrs_curr)

        # Computing global mean QRS length
        mean_qrs_global = np.mean(np.asarray(mean_qrs))

        self.num_leads = num_leads
        self.len_of_dels = len_of_dels
        self.ons = ons
        self.peaks = peaks
        self.offs = offs
        self.num_points = num_points
        self.mean_qrs = mean_qrs
        self.mean_qrs_global = mean_qrs_global

    def process(self, leads):
        self.__init__(leads)


class AllLeadsData:

    def __init__(self, del_data):

        # Computing params, which scales from mean QRS length
        loc = del_data.mean_qrs_global * float(QRSParams['DELTA_MEAN_QRS_LOC'])

        # Computing lead id with maximum number of dels
        max_dels_lead_id = np.argmax(np.asarray(del_data.len_of_dels))

        # Creating arrays with all complexes:
        ons_sum = []  # sum of onset values
        offs_sum = []  # sum of offset values
        borders_counts = []  # occurrence rate
        for del_id in range(0, del_data.len_of_dels[max_dels_lead_id]):
            ons_sum.append(del_data.ons[max_dels_lead_id][del_id])
            offs_sum.append(del_data.offs[max_dels_lead_id][del_id])
            borders_counts.append(1)

        del_candidates = {}  # array with special candidates for deletion

        # Filling arrays with all complexes:
        for lead_id in range(0, del_data.num_leads):

            # For all leads except init lead
            if lead_id != max_dels_lead_id:

                ons_lead = del_data.ons[lead_id]
                offs_lead = del_data.offs[lead_id]

                for del_id in range(0, del_data.len_of_dels[lead_id]):

                    curr_num_global = len(borders_counts)  # Current number of global complexes

                    on_diffs = []  # Differences between current onset and all global onsets (averaged)
                    off_diffs = []  # Differences between current offset and all global offsets (averaged)
                    for global_id in range(0, curr_num_global):
                        on_diffs.append(ons_lead[del_id] - ons_sum[global_id] / borders_counts[global_id])
                        off_diffs.append(offs_lead[del_id] - offs_sum[global_id] / borders_counts[global_id])

                    min_data = MinData(on_diffs, off_diffs)

                    # Calculate current optimal onset and offset
                    on_curr = ons_sum[min_data.on_argmin] / borders_counts[min_data.on_argmin] + on_diffs[min_data.on_argmin]
                    off_curr = offs_sum[min_data.off_argmin] / borders_counts[min_data.off_argmin] + off_diffs[min_data.off_argmin]

                    # If global closest onset and offset correspond to the same complexes
                    if min_data.on_argmin == min_data.off_argmin:

                        argmin = min_data.on_argmin

                        if (abs(min_data.on_min) < loc) or (abs(min_data.off_min) < loc):  # Global complex already exist

                            ons_sum[argmin] += on_curr
                            offs_sum[argmin] += off_curr
                            borders_counts[argmin] += 1

                        else:  # Need to insert additional global complex or delete special unique complex

                            if (on_diffs[argmin] < 0.0) and (off_diffs[argmin] < 0.0):
                                ons_sum.insert(argmin, on_curr)
                                offs_sum.insert(argmin, off_curr)
                                borders_counts.insert(argmin, 1)
                            elif (on_diffs[argmin] > 0.0) and (off_diffs[argmin] > 0.0):
                                ons_sum.insert(argmin + 1, on_curr)
                                offs_sum.insert(argmin + 1, off_curr)
                                borders_counts.insert(argmin + 1, 1)
                            else:
                                if lead_id in del_candidates:
                                    del_candidates[lead_id].append(del_id)
                                else:
                                    del_candidates[lead_id] = [del_id]
                    else:
                        warnings.warn("Onset and offset out of correspondence", UserWarning)

        self.ons_sum = ons_sum
        self.offs_sum = offs_sum
        self.borders_counts = borders_counts
        self.del_candidates = del_candidates


class MinData:

    def __init__(self, on_diffs, off_diffs):

        # Finding global onset closest to current onset
        on_argmin = np.argmin(np.absolute(np.asarray(on_diffs)))
        on_min = on_diffs[on_argmin]

        # Finding global offset closest to current offset
        off_argmin = np.argmin(np.absolute(np.asarray(off_diffs)))
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

        self.on_argmin = on_argmin
        self.on_min = on_min
        self.off_argmin = off_argmin
        self.off_min = off_min


class StatData:

    def __init__(self, leads, all_leads_data, del_data, corr_mtx):

        num_leads = len(leads)

        self.counts = []
        self.ons = []
        self.peaks = []
        self.offs = []

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

            self.counts.append(qrs_count)
            self.ons.append(qrs_ons)
            self.peaks.append(qrs_peaks)
            self.offs.append(qrs_offs)

