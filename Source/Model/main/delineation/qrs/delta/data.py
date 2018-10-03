import numpy as np
from Source.Model.main.params.qrs import QRSParams
from Source.Model.main.search.closest_position import *
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


class IntegralData:
    def __init__(self, leads, del_data):
        # Integral list
        integral = np.zeros(len(leads[0].origin))
        for lead_id in range(0, del_data.num_leads):
            for del_id in range(0, del_data.len_of_dels[lead_id]):
                for index in range(del_data.ons[lead_id][del_id], del_data.offs[lead_id][del_id] + 1):
                    integral[index] += 1

        # 'Common' lead
        integral_ons = []
        integral_offs = []
        positives = np.argwhere(np.asarray(integral) > 0)
        curr_pos = positives[0]
        integral_ons.append(positives[0])
        for pos in positives[1::]:
            if pos - curr_pos > 1:
                integral_offs.append(curr_pos)
                integral_ons.append(pos)
            curr_pos = pos
        integral_offs.append(positives[-1])

        num_dels = len(integral_ons)

        # Matrix of correspondence:
        mtx = []
        for lead_id in range(0, del_data.num_leads):
            lead_row = []
            lead_del_id = 0
            for del_id in range(0, num_dels):
                if del_data.ons[lead_id][lead_del_id] >= integral_ons[del_id] and del_data.offs[lead_id][lead_del_id] <= integral_offs[del_id]:
                    lead_row.append(lead_del_id)
                    lead_del_id += 1
                else:
                    lead_row.append(-1)
            mtx.append(lead_row)

        # Average data
        counts = np.zeros(num_dels)
        ons = [ [] for i in range(num_dels) ]
        peaks = [ [] for i in range(num_dels) ]
        offs = [ [] for i in range(num_dels) ]
        for del_id in range(0, num_dels):
            ons[del_id] = []
            peaks[del_id] = []
            offs[del_id] = []
            for lead_id in range(0, del_data.num_leads):
                if mtx[lead_id][del_id] >= 0:
                    counts[del_id] += 1
                    ons[del_id].append(del_data.ons[lead_id][mtx[lead_id][del_id]])
                    peaks[del_id].append(del_data.peaks[lead_id][mtx[lead_id][del_id]])
                    offs[del_id].append(del_data.offs[lead_id][mtx[lead_id][del_id]])

        self.num_dels = num_dels
        self.integral = integral
        self.integral_ons = integral_ons
        self.integral_offs = integral_offs

        self.mtx = mtx

        self.counts = counts
        self.ons = ons
        self.peaks = peaks
        self.offs = offs

