from Source.Model.main.zero_crossings.routines import *
from Source.Model.main.delineation.t.routines import *
from Source.Model.main.params.t import *


class TMorphologyData:

    def __init__(self, ecg_lead, delineation, target_scale_id):
        wdc_all_scales = ecg_lead.wdc

        onset_index = delineation.onset_index
        peak_index = delineation.peak_index
        offset_index = delineation.offset_index

        current_length = offset_index - onset_index

        begin_index = onset_index
        end_index = offset_index

        wdc = wdc_all_scales[target_scale_id]
        zcs = get_zcs_in_window(ecg_lead.zcs[target_scale_id], begin_index, end_index)

        if len(zcs) > 0:

            dels_zcs_ids = []
            peak_zc_id = 0
            min_dist = len(wdc)
            for zc_id in range(0, len(zcs)):
                dels_zcs_ids.append(zc_id)
                current_dist = abs(zcs[zc_id].index - peak_index)
                if current_dist < min_dist:
                    min_dist = current_dist
                    peak_zc_id = zc_id

            if zcs[peak_zc_id].extremum_sign is ExtremumSign.positive:
                t_sign = ExtremumSign.positive
            else:
                t_sign = ExtremumSign.negative

            self.begin_index = begin_index
            self.end_index = end_index
            self.length = current_length
            self.scale_id = target_scale_id
            self.wdc = wdc
            self.zcs = zcs
            self.dels_zcs_ids = dels_zcs_ids
            self.peak_zc_id = peak_zc_id
            self.t_sign = t_sign
            self.correct = 1

        else:
            self.correct = 0


