from Source.Model.main.zero_crossings.routines import *
from Source.Model.main.delineation.qrs.routines import *
from Source.Model.main.params.qrs import *


class QRSMorphologyData:

    def __init__(self, ecg_lead, delineation, target_scale_id):

        wdc = ecg_lead.wdc
        aux_wdc_scale_id = get_qrs_aux_wdc_scale_id(ecg_lead)
        num_scales = aux_wdc_scale_id + 1
        rate = ecg_lead.rate

        onset_index = delineation.onset_index
        peak_index = delineation.peak_index
        offset_index = delineation.offset_index

        normal_length = int(QRSParams['GAMMA_NORMAL_LENGTH'] * rate)
        current_length = offset_index - onset_index
        allowed_length_diff = normal_length - current_length

        if allowed_length_diff > 0:
            window_left = int(allowed_length_diff * QRSParams['GAMMA_ALLOWED_DIFF_PART_LEFT'])
            window_right = int(allowed_length_diff * QRSParams['GAMMA_ALLOWED_DIFF_PART_RIGHT'])
            if (onset_index - window_left) >= 0:
                begin_index = onset_index - window_left
            else:
                begin_index = 0
            end_index = offset_index + window_right
        else:
            window_left = 0
            window_right = 0
            begin_index = onset_index
            end_index = offset_index

        zcs = []  # List of all zcs in allowed interval
        dels_zcs_ids = []  # List of zcs ids, which corresponds current delineation
        peak_zcs_ids = []  # List of zcs ids, which corresponds peaks on different wdc scales

        q_signs = []
        r_signs = []
        s_signs = []

        for scale_id in range(0, aux_wdc_scale_id + 1):
            curr_wdc = wdc[scale_id]
            curr_zcs = get_zcs_in_window(ecg_lead.wdc[scale_id], ecg_lead.zcs[scale_id], begin_index, end_index)
            zcs.append(curr_zcs)

            curr_dels_zcs_ids = []
            peak_zc_id = 0
            min_dist = len(curr_wdc)
            for zc_id in range(0, len(curr_zcs)):
                if onset_index <= curr_zcs[zc_id].index <= offset_index:
                    curr_dels_zcs_ids.append(zc_id)
                    current_dist = abs(curr_zcs[zc_id].index - peak_index)
                    if current_dist < min_dist:
                        min_dist = current_dist
                        peak_zc_id = zc_id

            if len(curr_dels_zcs_ids) > 0 \
                    and peak_zc_id > curr_dels_zcs_ids[0] \
                    and curr_zcs[peak_zc_id - 1].g_ampl >= curr_zcs[peak_zc_id].g_ampl * float(QRSParams['GAMMA_R_NEG_PART']) \
                    and curr_zcs[peak_zc_id].extremum_sign is ExtremumSign.negative:
                peak_zc_id -= 1

            dels_zcs_ids.append(curr_dels_zcs_ids)
            peak_zcs_ids.append(peak_zc_id)

            if len(curr_zcs) > 0:
                if curr_zcs[peak_zc_id].extremum_sign is ExtremumSign.positive:
                    q_signs.append(ExtremumSign.negative)
                    r_signs.append(ExtremumSign.positive)
                    s_signs.append(ExtremumSign.negative)
                else:
                    q_signs.append(ExtremumSign.positive)
                    r_signs.append(ExtremumSign.negative)
                    s_signs.append(ExtremumSign.positive)

        self.window_left = window_left
        self.window_right = window_right
        self.begin_index = begin_index
        self.end_index = end_index
        self.num_scales = num_scales
        self.scale_id = target_scale_id
        self.wdc = wdc
        self.zcs = zcs
        self.dels_zcs_ids = dels_zcs_ids
        self.peak_zcs_ids = peak_zcs_ids
        self.allowed_length_diff = allowed_length_diff
        self.q_signs = q_signs
        self.r_signs = r_signs
        self.s_signs = s_signs

