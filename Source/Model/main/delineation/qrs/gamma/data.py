from Source.Model.main.zero_crossings.routines import *
from Source.Model.main.delineation.qrs.routines import *
from Source.Model.main.params.qrs import *


class QRSMorphologyData:

    def __init__(self, ecg_lead, delineation, target_scale_id):

        wdc = ecg_lead.wdc
        aux_wdc_scale_id = get_qrs_aux_wdc_scale_id(ecg_lead)
        num_scales = aux_wdc_scale_id + 1
        sampling_rate = ecg_lead.sampling_rate

        onset_index = delineation.onset_index
        peak_index = delineation.peak_index
        offset_index = delineation.offset_index

        normal_length = int(QRSParams['MORPHOLOGY_NORMAL'] * sampling_rate)
        current_length = offset_index - onset_index
        allowed_length_diff = normal_length - current_length

        if allowed_length_diff > 0:
            window_left = int(allowed_length_diff * QRSParams['MORPHOLOGY_ALLOWED_DIFF_PART_LEFT'])
            window_right = int(allowed_length_diff * QRSParams['MORPHOLOGY_ALLOWED_DIFF_PART_RIGHT'])
            begin_index = onset_index - window_left
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
            wdc_on_scale = wdc[scale_id]

            zcs_on_scale = get_zcs_with_global_mms(wdc_on_scale, begin_index, end_index)
            zcs.append(zcs_on_scale)

            current_dels_zcs_ids = []
            peak_zc_id = 0
            min_dist = len(wdc_on_scale)
            for zc_id in range(0, len(zcs_on_scale)):
                if onset_index <= zcs_on_scale[zc_id].index <= offset_index:
                    current_dels_zcs_ids.append(zc_id)
                    current_dist = abs(zcs_on_scale[zc_id].index - peak_index)
                    if current_dist < min_dist:
                        min_dist = current_dist
                        peak_zc_id = zc_id

            if len(current_dels_zcs_ids) > 0 \
                    and peak_zc_id > current_dels_zcs_ids[0] \
                    and zcs_on_scale[peak_zc_id - 1].mm_amplitude >= zcs_on_scale[peak_zc_id].mm_amplitude * float(QRSParams['MORPHOLOGY_R_NEG_PART']) \
                    and zcs_on_scale[peak_zc_id].extremum_sign is ExtremumSign.negative:
                peak_zc_id -= 1

            dels_zcs_ids.append(current_dels_zcs_ids)
            peak_zcs_ids.append(peak_zc_id)

            if len(zcs_on_scale) > 0:
                if zcs_on_scale[peak_zc_id].extremum_sign is ExtremumSign.positive:
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

