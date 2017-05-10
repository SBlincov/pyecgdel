from Source.Model.main.delineation.qrs.onset import *
from Source.Model.main.delineation.qrs.offset import *
from Source.Model.main.delineation.qrs.peak import *
from Source.Model.main.delineation.qrs.zcs import *
from Source.Model.main.delineation.qrs.routines import *
from Source.Model.main.params.qrs import *
from Source.Model.main.delineation.morfology_point import *


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


def get_qrs_morphology(ecg_lead, del_id, delineation):

    scale_id = 0

    qrs_morphology_data = QRSMorphologyData(ecg_lead, delineation, scale_id)
    r_zc_id = qrs_morphology_data.peak_zcs_ids[scale_id]

    is_left_complex, q_zc_id, left_points = is_left_qrs_morphology_complex(ecg_lead, qrs_morphology_data)
    is_right_complex, s_zc_id, right_points = is_right_qrs_morphology_complex(ecg_lead, qrs_morphology_data)

    if q_zc_id is not None:
        q_zc_id_diff = q_zc_id - r_zc_id
    else:
        q_zc_id_diff = -1

    if s_zc_id is not None:
        s_zc_id_diff = s_zc_id - r_zc_id
    else:
        s_zc_id_diff = 1

    branch_id = []

    if is_left_complex is True and is_right_complex is True:
        branch_id.append(1)
        points = borders_processing(ecg_lead, delineation, qrs_morphology_data,
                                    q_zc_id_diff, left_points,
                                    s_zc_id_diff, right_points,
                                    branch_id)

    elif is_left_complex is True and is_right_complex is False:
        branch_id.append(2)
        points = borders_processing(ecg_lead, delineation, qrs_morphology_data,
                                    q_zc_id_diff, left_points,
                                    s_zc_id_diff, right_points,
                                    branch_id)

    elif is_left_complex is False and is_right_complex is True:
        branch_id.append(3)
        points = borders_processing(ecg_lead, delineation, qrs_morphology_data,
                                    q_zc_id_diff, left_points,
                                    s_zc_id_diff, right_points,
                                    branch_id)

    else:
        branch_id.append(0)
        points = borders_processing(ecg_lead, delineation, qrs_morphology_data,
                                    q_zc_id_diff, left_points,
                                    s_zc_id_diff, right_points,
                                    branch_id)

    morphology = Morphology(del_id, points, branch_id)

    return morphology


def borders_processing(ecg_lead, delineation, qrs_morphology_data, q_zc_id_diff, left_points, s_zc_id_diff, right_points, branch_id):

    if is_r_in_del(qrs_morphology_data, q_zc_id_diff, s_zc_id_diff):
        branch_id.append(1)
        points = q_r_s_processing(ecg_lead, delineation, qrs_morphology_data, q_zc_id_diff, left_points, s_zc_id_diff, right_points)

    elif is_q_r_in_del(qrs_morphology_data, q_zc_id_diff, s_zc_id_diff):
        branch_id.append(2)
        points = q_r_s_processing(ecg_lead, delineation, qrs_morphology_data, q_zc_id_diff, left_points, s_zc_id_diff, right_points)

    elif is_r_s_in_del(qrs_morphology_data, q_zc_id_diff, s_zc_id_diff):
        branch_id.append(3)
        points = s_r_q_processing(ecg_lead, delineation, qrs_morphology_data, q_zc_id_diff, left_points, s_zc_id_diff, right_points)

    elif is_q_r_s_in_del(qrs_morphology_data, q_zc_id_diff, s_zc_id_diff):
        branch_id.append(4)
        points = q_r_s_processing(ecg_lead, delineation, qrs_morphology_data, q_zc_id_diff, left_points, s_zc_id_diff, right_points)

    elif is_extra_zcs_q_r_in_del(qrs_morphology_data, q_zc_id_diff, s_zc_id_diff):
        branch_id.append(5)
        points = q_r_s_processing(ecg_lead, delineation, qrs_morphology_data, q_zc_id_diff, left_points, s_zc_id_diff, right_points)

    elif is_p_zcs_q_r_in_del(qrs_morphology_data, q_zc_id_diff, s_zc_id_diff):
        branch_id.append(6)
        points = q_r_s_processing(ecg_lead, delineation, qrs_morphology_data, q_zc_id_diff, left_points, s_zc_id_diff, right_points)

    elif is_extra_zcs_q_r_s_in_del(qrs_morphology_data, q_zc_id_diff, s_zc_id_diff):
        branch_id.append(7)
        points = q_r_s_processing(ecg_lead, delineation, qrs_morphology_data, q_zc_id_diff, left_points, s_zc_id_diff, right_points)

    elif is_p_zcs_q_r_s_in_del(qrs_morphology_data, q_zc_id_diff, s_zc_id_diff):
        branch_id.append(8)
        points = q_r_s_processing(ecg_lead, delineation, qrs_morphology_data, q_zc_id_diff, left_points, s_zc_id_diff, right_points)

    elif is_r_s_extra_zcs_in_del(qrs_morphology_data, q_zc_id_diff, s_zc_id_diff):
        branch_id.append(9)
        points = s_r_q_processing(ecg_lead, delineation, qrs_morphology_data, q_zc_id_diff, left_points, s_zc_id_diff, right_points)

    elif is_r_s_t_zcs_in_del(qrs_morphology_data, q_zc_id_diff, s_zc_id_diff):
        branch_id.append(10)
        points = s_r_q_processing(ecg_lead, delineation, qrs_morphology_data, q_zc_id_diff, left_points, s_zc_id_diff, right_points)

    elif is_q_r_s_extra_zcs_in_del(qrs_morphology_data, q_zc_id_diff, s_zc_id_diff):
        branch_id.append(11)
        points = s_r_q_processing(ecg_lead, delineation, qrs_morphology_data, q_zc_id_diff, left_points, s_zc_id_diff, right_points)

    elif is_q_r_s_t_zcs_in_del(qrs_morphology_data, q_zc_id_diff, s_zc_id_diff):
        branch_id.append(12)
        points = s_r_q_processing(ecg_lead, delineation, qrs_morphology_data, q_zc_id_diff, left_points, s_zc_id_diff, right_points)

    elif is_extra_zcs_q_r_s_extra_zcs_in_del(qrs_morphology_data, q_zc_id_diff, s_zc_id_diff):
        branch_id.append(13)
        points = q_r_s_processing(ecg_lead, delineation, qrs_morphology_data, q_zc_id_diff, left_points, s_zc_id_diff, right_points)

    elif is_p_zcs_q_r_s_extra_zcs_in_del(qrs_morphology_data, q_zc_id_diff, s_zc_id_diff):
        branch_id.append(14)
        points = s_r_q_processing(ecg_lead, delineation, qrs_morphology_data, q_zc_id_diff, left_points, s_zc_id_diff, right_points)

    elif is_extra_zcs_q_r_s_t_zcs_in_del(qrs_morphology_data, q_zc_id_diff, s_zc_id_diff):
        branch_id.append(15)
        points = q_r_s_processing(ecg_lead, delineation, qrs_morphology_data, q_zc_id_diff, left_points, s_zc_id_diff, right_points)

    elif is_p_zcs_q_r_s_t_zcs_in_del(qrs_morphology_data, q_zc_id_diff, s_zc_id_diff):
        branch_id.append(16)
        points = q_r_s_processing(ecg_lead, delineation, qrs_morphology_data, q_zc_id_diff, left_points, s_zc_id_diff, right_points)

    else:
        # Default:
        branch_id.append(0)
        points = processing_default_morphology(ecg_lead, delineation, qrs_morphology_data)

    return points


def is_r_in_del(qrs_morphology_data, q_zc_id_diff, s_zc_id_diff):
    scale_id = qrs_morphology_data.scale_id
    zcs = qrs_morphology_data.zcs[scale_id]
    dels_zcs_ids = qrs_morphology_data.dels_zcs_ids[scale_id]
    peak_zc_id = qrs_morphology_data.peak_zcs_ids[scale_id]

    q_sign = qrs_morphology_data.q_signs[scale_id]
    r_sign = qrs_morphology_data.r_signs[scale_id]
    s_sign = qrs_morphology_data.s_signs[scale_id]

    r_zc_id = peak_zc_id
    q_zc_id = r_zc_id + q_zc_id_diff
    s_zc_id = r_zc_id + s_zc_id_diff

    r_zc_id_index = dels_zcs_ids.index(r_zc_id)
    q_zc_id_index = r_zc_id_index + q_zc_id_diff
    s_zc_id_index = r_zc_id_index + s_zc_id_diff

    real_dels_zcs_ids = dels_zcs_ids[0:q_zc_id_index + 1] + [dels_zcs_ids[r_zc_id_index]] + dels_zcs_ids[s_zc_id_index:]
    real_r_zc_id_index = real_dels_zcs_ids.index(r_zc_id)
    real_q_zc_id_index = real_r_zc_id_index - 1
    real_s_zc_id_index = real_r_zc_id_index + 1

    if len(real_dels_zcs_ids) is 1 \
            and real_r_zc_id_index == 0 \
            and zcs[r_zc_id].extremum_sign is r_sign:
        return True
    else:
        return False


def is_q_r_in_del(qrs_morphology_data, q_zc_id_diff, s_zc_id_diff):
    scale_id = qrs_morphology_data.scale_id
    zcs = qrs_morphology_data.zcs[scale_id]
    dels_zcs_ids = qrs_morphology_data.dels_zcs_ids[scale_id]
    peak_zc_id = qrs_morphology_data.peak_zcs_ids[scale_id]

    q_sign = qrs_morphology_data.q_signs[scale_id]
    r_sign = qrs_morphology_data.r_signs[scale_id]
    s_sign = qrs_morphology_data.s_signs[scale_id]

    r_zc_id = peak_zc_id
    q_zc_id = r_zc_id + q_zc_id_diff
    s_zc_id = r_zc_id + s_zc_id_diff

    r_zc_id_index = dels_zcs_ids.index(r_zc_id)
    q_zc_id_index = r_zc_id_index + q_zc_id_diff
    s_zc_id_index = r_zc_id_index + s_zc_id_diff

    real_dels_zcs_ids = dels_zcs_ids[0:q_zc_id_index + 1] + [dels_zcs_ids[r_zc_id_index]] + dels_zcs_ids[s_zc_id_index:]
    real_r_zc_id_index = real_dels_zcs_ids.index(r_zc_id)
    real_q_zc_id_index = real_r_zc_id_index - 1
    real_s_zc_id_index = real_r_zc_id_index + 1

    if len(real_dels_zcs_ids) is 2 \
            and real_r_zc_id_index == 1 \
            and zcs[q_zc_id].extremum_sign is q_sign \
            and zcs[r_zc_id].extremum_sign is r_sign:
        return True
    else:
        return False


def is_r_s_in_del(qrs_morphology_data, q_zc_id_diff, s_zc_id_diff):
    scale_id = qrs_morphology_data.scale_id
    zcs = qrs_morphology_data.zcs[scale_id]
    dels_zcs_ids = qrs_morphology_data.dels_zcs_ids[scale_id]
    peak_zc_id = qrs_morphology_data.peak_zcs_ids[scale_id]

    q_sign = qrs_morphology_data.q_signs[scale_id]
    r_sign = qrs_morphology_data.r_signs[scale_id]
    s_sign = qrs_morphology_data.s_signs[scale_id]

    r_zc_id = peak_zc_id
    q_zc_id = r_zc_id + q_zc_id_diff
    s_zc_id = r_zc_id + s_zc_id_diff

    r_zc_id_index = dels_zcs_ids.index(r_zc_id)
    q_zc_id_index = r_zc_id_index + q_zc_id_diff
    s_zc_id_index = r_zc_id_index + s_zc_id_diff

    real_dels_zcs_ids = dels_zcs_ids[0:q_zc_id_index + 1] + [dels_zcs_ids[r_zc_id_index]] + dels_zcs_ids[s_zc_id_index:]
    real_r_zc_id_index = real_dels_zcs_ids.index(r_zc_id)
    real_q_zc_id_index = real_r_zc_id_index - 1
    real_s_zc_id_index = real_r_zc_id_index + 1

    if len(real_dels_zcs_ids) is 2 \
            and real_r_zc_id_index == 0 \
            and zcs[r_zc_id].extremum_sign is r_sign \
            and zcs[s_zc_id].extremum_sign is s_sign:
        return True
    else:
        return False


def is_q_r_s_in_del(qrs_morphology_data, q_zc_id_diff, s_zc_id_diff):
    scale_id = qrs_morphology_data.scale_id
    zcs = qrs_morphology_data.zcs[scale_id]
    dels_zcs_ids = qrs_morphology_data.dels_zcs_ids[scale_id]
    peak_zc_id = qrs_morphology_data.peak_zcs_ids[scale_id]

    q_sign = qrs_morphology_data.q_signs[scale_id]
    r_sign = qrs_morphology_data.r_signs[scale_id]
    s_sign = qrs_morphology_data.s_signs[scale_id]

    r_zc_id = peak_zc_id
    q_zc_id = r_zc_id + q_zc_id_diff
    s_zc_id = r_zc_id + s_zc_id_diff

    r_zc_id_index = dels_zcs_ids.index(r_zc_id)
    q_zc_id_index = r_zc_id_index + q_zc_id_diff
    s_zc_id_index = r_zc_id_index + s_zc_id_diff

    real_dels_zcs_ids = dels_zcs_ids[0:q_zc_id_index + 1] + [dels_zcs_ids[r_zc_id_index]] + dels_zcs_ids[s_zc_id_index:]
    real_r_zc_id_index = real_dels_zcs_ids.index(r_zc_id)
    real_q_zc_id_index = real_r_zc_id_index - 1
    real_s_zc_id_index = real_r_zc_id_index + 1

    if len(real_dels_zcs_ids) is 3 \
            and real_r_zc_id_index == 1 \
            and zcs[q_zc_id].extremum_sign is q_sign \
            and zcs[r_zc_id].extremum_sign is r_sign \
            and zcs[s_zc_id].extremum_sign is s_sign:
        return True
    else:
        return False


def is_extra_zcs_q_r_in_del(qrs_morphology_data, q_zc_id_diff, s_zc_id_diff):
    scale_id = qrs_morphology_data.scale_id
    wdc = qrs_morphology_data.wdc[scale_id]
    zcs = qrs_morphology_data.zcs[scale_id]
    dels_zcs_ids = qrs_morphology_data.dels_zcs_ids[scale_id]
    peak_zc_id = qrs_morphology_data.peak_zcs_ids[scale_id]

    q_sign = qrs_morphology_data.q_signs[scale_id]
    r_sign = qrs_morphology_data.r_signs[scale_id]
    s_sign = qrs_morphology_data.s_signs[scale_id]

    r_zc_id = peak_zc_id
    q_zc_id = r_zc_id + q_zc_id_diff
    s_zc_id = r_zc_id + s_zc_id_diff

    r_zc_id_index = dels_zcs_ids.index(r_zc_id)
    q_zc_id_index = r_zc_id_index + q_zc_id_diff
    s_zc_id_index = r_zc_id_index + s_zc_id_diff

    real_dels_zcs_ids = dels_zcs_ids[0:q_zc_id_index + 1] + [dels_zcs_ids[r_zc_id_index]] + dels_zcs_ids[s_zc_id_index:]
    real_r_zc_id_index = real_dels_zcs_ids.index(r_zc_id)
    real_q_zc_id_index = real_r_zc_id_index - 1
    real_s_zc_id_index = real_r_zc_id_index + 1

    mm_small_left = zcs[peak_zc_id].mm_amplitude * float(QRSParams['MORPHOLOGY_MM_SMALL_PART_LEFT'])

    if len(real_dels_zcs_ids) > 2 \
            and real_r_zc_id_index == len(real_dels_zcs_ids) - 1 \
            and zcs[q_zc_id].extremum_sign is q_sign \
            and zcs[r_zc_id].extremum_sign is r_sign:

        if q_zc_id - 1 >= dels_zcs_ids[0]:
            mm_left = find_left_mm(zcs[q_zc_id - 1].index, wdc)
            if abs(mm_left.value) < mm_small_left:
                return True

    else:
        return False


def is_p_zcs_q_r_in_del(qrs_morphology_data, q_zc_id_diff, s_zc_id_diff):
    scale_id = qrs_morphology_data.scale_id
    wdc = qrs_morphology_data.wdc[scale_id]
    zcs = qrs_morphology_data.zcs[scale_id]
    dels_zcs_ids = qrs_morphology_data.dels_zcs_ids[scale_id]
    peak_zc_id = qrs_morphology_data.peak_zcs_ids[scale_id]

    q_sign = qrs_morphology_data.q_signs[scale_id]
    r_sign = qrs_morphology_data.r_signs[scale_id]
    s_sign = qrs_morphology_data.s_signs[scale_id]

    r_zc_id = peak_zc_id
    q_zc_id = r_zc_id + q_zc_id_diff
    s_zc_id = r_zc_id + s_zc_id_diff

    r_zc_id_index = dels_zcs_ids.index(r_zc_id)
    q_zc_id_index = r_zc_id_index + q_zc_id_diff
    s_zc_id_index = r_zc_id_index + s_zc_id_diff

    real_dels_zcs_ids = dels_zcs_ids[0:q_zc_id_index + 1] + [dels_zcs_ids[r_zc_id_index]] + dels_zcs_ids[s_zc_id_index:]
    real_r_zc_id_index = real_dels_zcs_ids.index(r_zc_id)
    real_q_zc_id_index = real_r_zc_id_index - 1
    real_s_zc_id_index = real_r_zc_id_index + 1

    mm_small_left = zcs[peak_zc_id].mm_amplitude * float(QRSParams['MORPHOLOGY_MM_SMALL_PART_LEFT'])

    if len(real_dels_zcs_ids) > 2 \
            and real_r_zc_id_index == len(real_dels_zcs_ids) - 1 \
            and zcs[q_zc_id].extremum_sign is q_sign \
            and zcs[r_zc_id].extremum_sign is r_sign:

        if q_zc_id - 1 >= dels_zcs_ids[0]:
            mm_left = find_left_mm(zcs[q_zc_id - 1].index, wdc)
            if abs(mm_left.value) > mm_small_left:
                return True

    else:
        return False


def is_extra_zcs_q_r_s_in_del(qrs_morphology_data, q_zc_id_diff, s_zc_id_diff):
    scale_id = qrs_morphology_data.scale_id
    wdc = qrs_morphology_data.wdc[scale_id]
    zcs = qrs_morphology_data.zcs[scale_id]
    dels_zcs_ids = qrs_morphology_data.dels_zcs_ids[scale_id]
    peak_zc_id = qrs_morphology_data.peak_zcs_ids[scale_id]

    q_sign = qrs_morphology_data.q_signs[scale_id]
    r_sign = qrs_morphology_data.r_signs[scale_id]
    s_sign = qrs_morphology_data.s_signs[scale_id]

    r_zc_id = peak_zc_id
    q_zc_id = r_zc_id + q_zc_id_diff
    s_zc_id = r_zc_id + s_zc_id_diff

    r_zc_id_index = dels_zcs_ids.index(r_zc_id)
    q_zc_id_index = r_zc_id_index + q_zc_id_diff
    s_zc_id_index = r_zc_id_index + s_zc_id_diff

    real_dels_zcs_ids = dels_zcs_ids[0:q_zc_id_index + 1] + [dels_zcs_ids[r_zc_id_index]] + dels_zcs_ids[s_zc_id_index:]
    real_r_zc_id_index = real_dels_zcs_ids.index(r_zc_id)
    real_q_zc_id_index = real_r_zc_id_index - 1
    real_s_zc_id_index = real_r_zc_id_index + 1

    mm_small_left = zcs[peak_zc_id].mm_amplitude * float(QRSParams['MORPHOLOGY_MM_SMALL_PART_LEFT'])

    if len(real_dels_zcs_ids) > 3 \
            and real_r_zc_id_index == len(real_dels_zcs_ids) - 2 \
            and zcs[q_zc_id].extremum_sign is q_sign \
            and zcs[r_zc_id].extremum_sign is r_sign \
            and zcs[s_zc_id].extremum_sign is s_sign:

        if q_zc_id - 1 >= dels_zcs_ids[0]:
            mm_left = find_left_mm(zcs[q_zc_id - 1].index, wdc)
            if abs(mm_left.value) < mm_small_left:
                return True

    else:
        return False


def is_p_zcs_q_r_s_in_del(qrs_morphology_data, q_zc_id_diff, s_zc_id_diff):
    scale_id = qrs_morphology_data.scale_id
    wdc = qrs_morphology_data.wdc[scale_id]
    zcs = qrs_morphology_data.zcs[scale_id]
    dels_zcs_ids = qrs_morphology_data.dels_zcs_ids[scale_id]
    peak_zc_id = qrs_morphology_data.peak_zcs_ids[scale_id]

    q_sign = qrs_morphology_data.q_signs[scale_id]
    r_sign = qrs_morphology_data.r_signs[scale_id]
    s_sign = qrs_morphology_data.s_signs[scale_id]

    r_zc_id = peak_zc_id
    q_zc_id = r_zc_id + q_zc_id_diff
    s_zc_id = r_zc_id + s_zc_id_diff

    r_zc_id_index = dels_zcs_ids.index(r_zc_id)
    q_zc_id_index = r_zc_id_index + q_zc_id_diff
    s_zc_id_index = r_zc_id_index + s_zc_id_diff

    real_dels_zcs_ids = dels_zcs_ids[0:q_zc_id_index + 1] + [dels_zcs_ids[r_zc_id_index]] + dels_zcs_ids[s_zc_id_index:]
    real_r_zc_id_index = real_dels_zcs_ids.index(r_zc_id)
    real_q_zc_id_index = real_r_zc_id_index - 1
    real_s_zc_id_index = real_r_zc_id_index + 1

    mm_small_left = zcs[peak_zc_id].mm_amplitude * float(QRSParams['MORPHOLOGY_MM_SMALL_PART_LEFT'])

    if len(real_dels_zcs_ids) > 3 \
            and real_r_zc_id_index == len(real_dels_zcs_ids) - 2 \
            and zcs[q_zc_id].extremum_sign is q_sign \
            and zcs[r_zc_id].extremum_sign is r_sign \
            and zcs[s_zc_id].extremum_sign is s_sign:

        if q_zc_id - 1 >= dels_zcs_ids[0]:
            mm_left = find_left_mm(zcs[q_zc_id - 1].index, wdc)
            if abs(mm_left.value) > mm_small_left:
                return True

    else:
        return False


def is_r_s_extra_zcs_in_del(qrs_morphology_data, q_zc_id_diff, s_zc_id_diff):
    scale_id = qrs_morphology_data.scale_id
    wdc = qrs_morphology_data.wdc[scale_id]
    zcs = qrs_morphology_data.zcs[scale_id]
    dels_zcs_ids = qrs_morphology_data.dels_zcs_ids[scale_id]
    peak_zc_id = qrs_morphology_data.peak_zcs_ids[scale_id]

    q_sign = qrs_morphology_data.q_signs[scale_id]
    r_sign = qrs_morphology_data.r_signs[scale_id]
    s_sign = qrs_morphology_data.s_signs[scale_id]

    r_zc_id = peak_zc_id
    q_zc_id = r_zc_id + q_zc_id_diff
    s_zc_id = r_zc_id + s_zc_id_diff

    r_zc_id_index = dels_zcs_ids.index(r_zc_id)
    q_zc_id_index = r_zc_id_index + q_zc_id_diff
    s_zc_id_index = r_zc_id_index + s_zc_id_diff

    real_dels_zcs_ids = dels_zcs_ids[0:q_zc_id_index + 1] + [dels_zcs_ids[r_zc_id_index]] + dels_zcs_ids[s_zc_id_index:]
    real_r_zc_id_index = real_dels_zcs_ids.index(r_zc_id)
    real_q_zc_id_index = real_r_zc_id_index - 1
    real_s_zc_id_index = real_r_zc_id_index + 1

    mm_small_right = zcs[peak_zc_id].mm_amplitude * float(QRSParams['MORPHOLOGY_MM_SMALL_PART_RIGHT'])

    if len(real_dels_zcs_ids) > 2 \
            and real_r_zc_id_index == 0 \
            and zcs[r_zc_id].extremum_sign is r_sign \
            and zcs[s_zc_id].extremum_sign is s_sign:

        if s_zc_id + 1 < dels_zcs_ids[0] + len(dels_zcs_ids):
            mm_right = find_right_mm(zcs[s_zc_id + 1].index, wdc)
            if abs(mm_right.value) < mm_small_right:
                return True

    else:
        return False


def is_r_s_t_zcs_in_del(qrs_morphology_data, q_zc_id_diff, s_zc_id_diff):
    scale_id = qrs_morphology_data.scale_id
    wdc = qrs_morphology_data.wdc[scale_id]
    zcs = qrs_morphology_data.zcs[scale_id]
    dels_zcs_ids = qrs_morphology_data.dels_zcs_ids[scale_id]
    peak_zc_id = qrs_morphology_data.peak_zcs_ids[scale_id]

    q_sign = qrs_morphology_data.q_signs[scale_id]
    r_sign = qrs_morphology_data.r_signs[scale_id]
    s_sign = qrs_morphology_data.s_signs[scale_id]

    r_zc_id = peak_zc_id
    q_zc_id = r_zc_id + q_zc_id_diff
    s_zc_id = r_zc_id + s_zc_id_diff

    r_zc_id_index = dels_zcs_ids.index(r_zc_id)
    q_zc_id_index = r_zc_id_index + q_zc_id_diff
    s_zc_id_index = r_zc_id_index + s_zc_id_diff

    real_dels_zcs_ids = dels_zcs_ids[0:q_zc_id_index + 1] + [dels_zcs_ids[r_zc_id_index]] + dels_zcs_ids[s_zc_id_index:]
    real_r_zc_id_index = real_dels_zcs_ids.index(r_zc_id)
    real_q_zc_id_index = real_r_zc_id_index - 1
    real_s_zc_id_index = real_r_zc_id_index + 1

    mm_small_right = zcs[peak_zc_id].mm_amplitude * float(QRSParams['MORPHOLOGY_MM_SMALL_PART_RIGHT'])

    if len(real_dels_zcs_ids) > 2 \
            and real_r_zc_id_index == 0 \
            and zcs[r_zc_id].extremum_sign is r_sign \
            and zcs[s_zc_id].extremum_sign is s_sign:

        if s_zc_id + 1 < dels_zcs_ids[0] + len(dels_zcs_ids):
            mm_right = find_right_mm(zcs[s_zc_id + 1].index, wdc)
            if abs(mm_right.value) > mm_small_right:
                return True

    else:
        return False


def is_q_r_s_extra_zcs_in_del(qrs_morphology_data, q_zc_id_diff, s_zc_id_diff):
    scale_id = qrs_morphology_data.scale_id
    wdc = qrs_morphology_data.wdc[scale_id]
    zcs = qrs_morphology_data.zcs[scale_id]
    dels_zcs_ids = qrs_morphology_data.dels_zcs_ids[scale_id]
    peak_zc_id = qrs_morphology_data.peak_zcs_ids[scale_id]

    q_sign = qrs_morphology_data.q_signs[scale_id]
    r_sign = qrs_morphology_data.r_signs[scale_id]
    s_sign = qrs_morphology_data.s_signs[scale_id]

    r_zc_id = peak_zc_id
    q_zc_id = r_zc_id + q_zc_id_diff
    s_zc_id = r_zc_id + s_zc_id_diff

    r_zc_id_index = dels_zcs_ids.index(r_zc_id)
    q_zc_id_index = r_zc_id_index + q_zc_id_diff
    s_zc_id_index = r_zc_id_index + s_zc_id_diff

    real_dels_zcs_ids = dels_zcs_ids[0:q_zc_id_index + 1] + [dels_zcs_ids[r_zc_id_index]] + dels_zcs_ids[s_zc_id_index:]
    real_r_zc_id_index = real_dels_zcs_ids.index(r_zc_id)
    real_q_zc_id_index = real_r_zc_id_index - 1
    real_s_zc_id_index = real_r_zc_id_index + 1

    mm_small_right = zcs[peak_zc_id].mm_amplitude * float(QRSParams['MORPHOLOGY_MM_SMALL_PART_RIGHT'])

    if len(real_dels_zcs_ids) > 3 \
            and real_r_zc_id_index == 1 \
            and zcs[q_zc_id].extremum_sign is q_sign \
            and zcs[r_zc_id].extremum_sign is r_sign \
            and zcs[s_zc_id].extremum_sign is s_sign:

        if s_zc_id + 1 < dels_zcs_ids[0] + len(dels_zcs_ids):
            mm_right = find_right_mm(zcs[s_zc_id + 1].index, wdc)
            if abs(mm_right.value) < mm_small_right:
                return True

    else:
        return False


def is_q_r_s_t_zcs_in_del(qrs_morphology_data, q_zc_id_diff, s_zc_id_diff):
    scale_id = qrs_morphology_data.scale_id
    wdc = qrs_morphology_data.wdc[scale_id]
    zcs = qrs_morphology_data.zcs[scale_id]
    dels_zcs_ids = qrs_morphology_data.dels_zcs_ids[scale_id]
    peak_zc_id = qrs_morphology_data.peak_zcs_ids[scale_id]

    q_sign = qrs_morphology_data.q_signs[scale_id]
    r_sign = qrs_morphology_data.r_signs[scale_id]
    s_sign = qrs_morphology_data.s_signs[scale_id]

    r_zc_id = peak_zc_id
    q_zc_id = r_zc_id + q_zc_id_diff
    s_zc_id = r_zc_id + s_zc_id_diff

    r_zc_id_index = dels_zcs_ids.index(r_zc_id)
    q_zc_id_index = r_zc_id_index + q_zc_id_diff
    s_zc_id_index = r_zc_id_index + s_zc_id_diff

    real_dels_zcs_ids = dels_zcs_ids[0:q_zc_id_index + 1] + [dels_zcs_ids[r_zc_id_index]] + dels_zcs_ids[s_zc_id_index:]
    real_r_zc_id_index = real_dels_zcs_ids.index(r_zc_id)
    real_q_zc_id_index = real_r_zc_id_index - 1
    real_s_zc_id_index = real_r_zc_id_index + 1

    mm_small_right = zcs[peak_zc_id].mm_amplitude * float(QRSParams['MORPHOLOGY_MM_SMALL_PART_RIGHT'])

    if len(real_dels_zcs_ids) > 3 \
            and real_r_zc_id_index == 1 \
            and zcs[q_zc_id].extremum_sign is q_sign \
            and zcs[r_zc_id].extremum_sign is r_sign \
            and zcs[s_zc_id].extremum_sign is s_sign:

        if s_zc_id + 1 < dels_zcs_ids[0] + len(dels_zcs_ids):
            mm_right = find_right_mm(zcs[s_zc_id + 1].index, wdc)
            if abs(mm_right.value) > mm_small_right:
                return True

    else:
        return False


def is_extra_zcs_q_r_s_extra_zcs_in_del(qrs_morphology_data, q_zc_id_diff, s_zc_id_diff):
    scale_id = qrs_morphology_data.scale_id
    wdc = qrs_morphology_data.wdc[scale_id]
    zcs = qrs_morphology_data.zcs[scale_id]
    dels_zcs_ids = qrs_morphology_data.dels_zcs_ids[scale_id]
    peak_zc_id = qrs_morphology_data.peak_zcs_ids[scale_id]

    q_sign = qrs_morphology_data.q_signs[scale_id]
    r_sign = qrs_morphology_data.r_signs[scale_id]
    s_sign = qrs_morphology_data.s_signs[scale_id]

    r_zc_id = peak_zc_id
    q_zc_id = r_zc_id + q_zc_id_diff
    s_zc_id = r_zc_id + s_zc_id_diff

    r_zc_id_index = dels_zcs_ids.index(r_zc_id)
    q_zc_id_index = r_zc_id_index + q_zc_id_diff
    s_zc_id_index = r_zc_id_index + s_zc_id_diff

    real_dels_zcs_ids = dels_zcs_ids[0:q_zc_id_index + 1] + [dels_zcs_ids[r_zc_id_index]] + dels_zcs_ids[s_zc_id_index:]
    real_r_zc_id_index = real_dels_zcs_ids.index(r_zc_id)
    real_q_zc_id_index = real_r_zc_id_index - 1
    real_s_zc_id_index = real_r_zc_id_index + 1

    mm_small_left = zcs[peak_zc_id].mm_amplitude * float(QRSParams['MORPHOLOGY_MM_SMALL_PART_LEFT'])
    mm_small_right = zcs[peak_zc_id].mm_amplitude * float(QRSParams['MORPHOLOGY_MM_SMALL_PART_RIGHT'])

    if len(real_dels_zcs_ids) > 4 \
            and 2 <= real_r_zc_id_index < len(real_dels_zcs_ids) - 2 \
            and zcs[q_zc_id].extremum_sign is q_sign \
            and zcs[r_zc_id].extremum_sign is r_sign \
            and zcs[s_zc_id].extremum_sign is s_sign:

        if q_zc_id - 1 >= dels_zcs_ids[0] and s_zc_id + 1 < dels_zcs_ids[0] + len(dels_zcs_ids):
            mm_left = find_left_mm(zcs[q_zc_id - 1].index, wdc)
            mm_right = find_right_mm(zcs[s_zc_id + 1].index, wdc)
            if abs(mm_left.value) < mm_small_left and abs(mm_right.value) < mm_small_right:
                return True

    else:
        return False


def is_p_zcs_q_r_s_extra_zcs_in_del(qrs_morphology_data, q_zc_id_diff, s_zc_id_diff):
    scale_id = qrs_morphology_data.scale_id
    wdc = qrs_morphology_data.wdc[scale_id]
    zcs = qrs_morphology_data.zcs[scale_id]
    dels_zcs_ids = qrs_morphology_data.dels_zcs_ids[scale_id]
    peak_zc_id = qrs_morphology_data.peak_zcs_ids[scale_id]

    q_sign = qrs_morphology_data.q_signs[scale_id]
    r_sign = qrs_morphology_data.r_signs[scale_id]
    s_sign = qrs_morphology_data.s_signs[scale_id]

    r_zc_id = peak_zc_id
    q_zc_id = r_zc_id + q_zc_id_diff
    s_zc_id = r_zc_id + s_zc_id_diff

    r_zc_id_index = dels_zcs_ids.index(r_zc_id)
    q_zc_id_index = r_zc_id_index + q_zc_id_diff
    s_zc_id_index = r_zc_id_index + s_zc_id_diff

    real_dels_zcs_ids = dels_zcs_ids[0:q_zc_id_index + 1] + [dels_zcs_ids[r_zc_id_index]] + dels_zcs_ids[s_zc_id_index:]
    real_r_zc_id_index = real_dels_zcs_ids.index(r_zc_id)
    real_q_zc_id_index = real_r_zc_id_index - 1
    real_s_zc_id_index = real_r_zc_id_index + 1

    mm_small_left = zcs[peak_zc_id].mm_amplitude * float(QRSParams['MORPHOLOGY_MM_SMALL_PART_LEFT'])
    mm_small_right = zcs[peak_zc_id].mm_amplitude * float(QRSParams['MORPHOLOGY_MM_SMALL_PART_RIGHT'])

    if len(real_dels_zcs_ids) > 4 \
            and 2 <= real_r_zc_id_index < len(real_dels_zcs_ids) - 2 \
            and zcs[q_zc_id].extremum_sign is q_sign \
            and zcs[r_zc_id].extremum_sign is r_sign \
            and zcs[s_zc_id].extremum_sign is s_sign:

        if q_zc_id - 1 >= dels_zcs_ids[0] and s_zc_id + 1 < dels_zcs_ids[0] + len(dels_zcs_ids):
            mm_left = find_left_mm(zcs[q_zc_id - 1].index, wdc)
            mm_right = find_right_mm(zcs[s_zc_id + 1].index, wdc)
            if abs(mm_left.value) > mm_small_left and abs(mm_right.value) < mm_small_right:
                return True

    else:
        return False


def is_extra_zcs_q_r_s_t_zcs_in_del(qrs_morphology_data, q_zc_id_diff, s_zc_id_diff):
    scale_id = qrs_morphology_data.scale_id
    wdc = qrs_morphology_data.wdc[scale_id]
    zcs = qrs_morphology_data.zcs[scale_id]
    dels_zcs_ids = qrs_morphology_data.dels_zcs_ids[scale_id]
    peak_zc_id = qrs_morphology_data.peak_zcs_ids[scale_id]

    q_sign = qrs_morphology_data.q_signs[scale_id]
    r_sign = qrs_morphology_data.r_signs[scale_id]
    s_sign = qrs_morphology_data.s_signs[scale_id]

    r_zc_id = peak_zc_id
    q_zc_id = r_zc_id + q_zc_id_diff
    s_zc_id = r_zc_id + s_zc_id_diff

    r_zc_id_index = dels_zcs_ids.index(r_zc_id)
    q_zc_id_index = r_zc_id_index + q_zc_id_diff
    s_zc_id_index = r_zc_id_index + s_zc_id_diff

    real_dels_zcs_ids = dels_zcs_ids[0:q_zc_id_index + 1] + [dels_zcs_ids[r_zc_id_index]] + dels_zcs_ids[s_zc_id_index:]
    real_r_zc_id_index = real_dels_zcs_ids.index(r_zc_id)
    real_q_zc_id_index = real_r_zc_id_index - 1
    real_s_zc_id_index = real_r_zc_id_index + 1

    mm_small_left = zcs[peak_zc_id].mm_amplitude * float(QRSParams['MORPHOLOGY_MM_SMALL_PART_LEFT'])
    mm_small_right = zcs[peak_zc_id].mm_amplitude * float(QRSParams['MORPHOLOGY_MM_SMALL_PART_RIGHT'])

    if len(real_dels_zcs_ids) > 4 \
            and 2 <= real_r_zc_id_index < len(real_dels_zcs_ids) - 2 \
            and zcs[q_zc_id].extremum_sign is q_sign \
            and zcs[r_zc_id].extremum_sign is r_sign \
            and zcs[s_zc_id].extremum_sign is s_sign:

        if q_zc_id - 1 >= dels_zcs_ids[0] and s_zc_id + 1 < dels_zcs_ids[0] + len(dels_zcs_ids):
            mm_left = find_left_mm(zcs[q_zc_id - 1].index, wdc)
            mm_right = find_right_mm(zcs[s_zc_id + 1].index, wdc)
            if abs(mm_left.value) < mm_small_left and abs(mm_right.value) > mm_small_right:
                return True

    else:
        return False


def is_p_zcs_q_r_s_t_zcs_in_del(qrs_morphology_data, q_zc_id_diff, s_zc_id_diff):
    scale_id = qrs_morphology_data.scale_id
    wdc = qrs_morphology_data.wdc[scale_id]
    zcs = qrs_morphology_data.zcs[scale_id]
    dels_zcs_ids = qrs_morphology_data.dels_zcs_ids[scale_id]
    peak_zc_id = qrs_morphology_data.peak_zcs_ids[scale_id]

    q_sign = qrs_morphology_data.q_signs[scale_id]
    r_sign = qrs_morphology_data.r_signs[scale_id]
    s_sign = qrs_morphology_data.s_signs[scale_id]

    r_zc_id = peak_zc_id
    q_zc_id = r_zc_id + q_zc_id_diff
    s_zc_id = r_zc_id + s_zc_id_diff

    r_zc_id_index = dels_zcs_ids.index(r_zc_id)
    q_zc_id_index = r_zc_id_index + q_zc_id_diff
    s_zc_id_index = r_zc_id_index + s_zc_id_diff

    real_dels_zcs_ids = dels_zcs_ids[0:q_zc_id_index + 1] + [dels_zcs_ids[r_zc_id_index]] + dels_zcs_ids[s_zc_id_index:]
    real_r_zc_id_index = real_dels_zcs_ids.index(r_zc_id)
    real_q_zc_id_index = real_r_zc_id_index - 1
    real_s_zc_id_index = real_r_zc_id_index + 1

    mm_small_left = zcs[peak_zc_id].mm_amplitude * float(QRSParams['MORPHOLOGY_MM_SMALL_PART_LEFT'])
    mm_small_right = zcs[peak_zc_id].mm_amplitude * float(QRSParams['MORPHOLOGY_MM_SMALL_PART_RIGHT'])

    if len(real_dels_zcs_ids) > 4 \
            and 2 <= real_r_zc_id_index < len(real_dels_zcs_ids) - 2 \
            and zcs[q_zc_id].extremum_sign is q_sign \
            and zcs[r_zc_id].extremum_sign is r_sign \
            and zcs[s_zc_id].extremum_sign is s_sign:

        if q_zc_id - 1 >= dels_zcs_ids[0] and s_zc_id + 1 < dels_zcs_ids[0] + len(dels_zcs_ids):
            mm_left = find_left_mm(zcs[q_zc_id - 1].index, wdc)
            mm_right = find_right_mm(zcs[s_zc_id + 1].index, wdc)
            if abs(mm_left.value) > mm_small_left and abs(mm_right.value) > mm_small_right:
                return True

    else:
        return False


def q_processing(q_zc_id, ecg_lead, delineation, qrs_morphology_data, points, direction):
    scale_id = qrs_morphology_data.scale_id
    wdc = qrs_morphology_data.wdc[scale_id]
    zcs = qrs_morphology_data.zcs[scale_id]
    peak_zc_id = qrs_morphology_data.peak_zcs_ids[scale_id]
    begin_index = qrs_morphology_data.begin_index

    q_zc_sign = qrs_morphology_data.q_signs[scale_id]

    mm_small_left = zcs[peak_zc_id].mm_amplitude * float(QRSParams['MORPHOLOGY_MM_SMALL_PART_LEFT'])

    onset_index = delineation.onset_index

    if q_zc_id >= 0 and zcs[q_zc_id].extremum_sign is q_zc_sign:

        q_index = zcs[q_zc_id].index
        q_value = ecg_lead.filtrated[q_index]
        if q_zc_sign is ExtremumSign.positive:
            q_sign = WaveSign.positive
        else:
            q_sign = WaveSign.negative
        q_point = Point(PointName.q, q_index, q_value, q_sign)

        mm_curr = find_left_mm(q_index, wdc)
        mm_next = mm_curr
        mms = []
        mms_zc = []
        # While mms have the same sign and take place in allowed interval
        while mm_curr.index > begin_index:

            if mm_curr.value * mm_next.value < 0:
                mms_zc.append(mm_next)

            mm_curr = mm_next
            mms.append(mm_curr)
            mm_next = find_left_mm(mm_curr.index - 1, wdc)

        qrs_onset_index = begin_index

        if mms:
            # Default way for offset
            mm_onset = mms[0]
            is_onset_on_mm = True

            if len(mms) > 1:

                if len(mms_zc) > 1 and mms_zc[0].index > qrs_onset_index and abs(mms_zc[0].value) < mm_small_left:
                    # Firstly locking for zc with small right mm. This zc corresponds to offset
                    qrs_onset_index = find_right_thc_index(wdc, mms_zc[0].index, mms[0].index, 0.0)
                    is_onset_on_mm = False

                else:
                    # The second mm in mms is incorrect, which corresponds to offset
                    if not mms[1].correctness:
                        mm_onset = mms[1]
                        is_onset_on_mm = True

            if is_onset_on_mm and mm_onset.index > qrs_onset_index:
                qrs_onset_index = mm_onset.index

        qrs_onset_value = ecg_lead.filtrated[qrs_onset_index]
        qrs_onset_sign = WaveSign.none
        qrs_onset_point = Point(PointName.qrs_onset, qrs_onset_index, qrs_onset_value, qrs_onset_sign)

        if q_index > qrs_onset_index:
            points.insert(0, q_point)

        if direction < 0:
            points.insert(0, qrs_onset_point)
        else:
            points.append(qrs_onset_point)

        delineation.onset_index = qrs_onset_index

    else:

        qrs_onset_index = onset_index
        qrs_onset_value = ecg_lead.filtrated[qrs_onset_index]
        qrs_onset_sign = WaveSign.none
        qrs_onset_point = Point(PointName.qrs_onset, qrs_onset_index, qrs_onset_value, qrs_onset_sign)
        if direction < 0:
            points.insert(0, qrs_onset_point)
        else:
            points.append(qrs_onset_point)


def r_processing(r_zc_id, ecg_lead, delineation, qrs_morphology_data, points, direction):
    scale_id = qrs_morphology_data.scale_id
    zcs = qrs_morphology_data.zcs[scale_id]

    r_zc_sign = qrs_morphology_data.r_signs[scale_id]

    r_index = zcs[r_zc_id].index
    r_value = ecg_lead.filtrated[r_index]
    if r_zc_sign is ExtremumSign.positive:
        r_sign = WaveSign.positive
    else:
        r_sign = WaveSign.negative
    r_point = Point(PointName.r, r_index, r_value, r_sign)
    if direction < 0:
        points.insert(0, r_point)
    else:
        points.append(r_point)

    delineation.peak_index = r_index


def s_processing(s_zc_id, ecg_lead, delineation, qrs_morphology_data, points, direction):
    scale_id = qrs_morphology_data.scale_id
    wdc = qrs_morphology_data.wdc[scale_id]
    zcs = qrs_morphology_data.zcs[scale_id]
    peak_zc_id = qrs_morphology_data.peak_zcs_ids[scale_id]
    end_index = qrs_morphology_data.end_index

    s_zc_sign = qrs_morphology_data.q_signs[scale_id]

    mm_small_right = zcs[peak_zc_id].mm_amplitude * float(QRSParams['MORPHOLOGY_MM_SMALL_PART_RIGHT'])

    offset_index = delineation.offset_index

    if s_zc_id < len(zcs) and zcs[s_zc_id].extremum_sign is ExtremumSign.negative:

        s_index = zcs[s_zc_id].index
        s_value = ecg_lead.filtrated[s_index]
        if s_zc_sign is ExtremumSign.positive:
            s_sign = WaveSign.positive
        else:
            s_sign = WaveSign.negative
        s_point = Point(PointName.s, s_index, s_value, s_sign)

        mm_curr = find_right_mm(s_index, wdc)
        mm_next = mm_curr
        mms = []
        mms_zc = []
        # While mms have the same sign and take place in allowed interval
        while mm_curr.index < end_index:

            if mm_curr.value * mm_next.value < 0:
                mms_zc.append(mm_next)

            mm_curr = mm_next
            mms.append(mm_curr)
            mm_next = find_right_mm(mm_curr.index + 1, wdc)

        qrs_offset_index = end_index

        if mms:
            # Default way for offset
            mm_offset = mms[0]
            is_offset_on_mm = True

            if len(mms) > 1:

                if len(mms_zc) > 1 and mms_zc[0].index < qrs_offset_index and abs(mms_zc[0].value) < mm_small_right:
                    # Firstly locking for zc with small right mm. This zc corresponds to offset
                    qrs_offset_index = find_left_thc_index(wdc, mms_zc[0].index, mms[0].index, 0.0)
                    is_offset_on_mm = False

                else:
                    # The second mm in mms is incorrect, which corresponds to offset
                    if not mms[1].correctness:
                        mm_offset = mms[1]
                        is_offset_on_mm = True

            if is_offset_on_mm and mm_offset.index < qrs_offset_index:
                qrs_offset_index = mm_offset.index

        qrs_offset_value = ecg_lead.filtrated[qrs_offset_index]
        qrs_offset_sign = WaveSign.none
        qrs_offset_point = Point(PointName.qrs_offset, qrs_offset_index, qrs_offset_value, qrs_offset_sign)

        if s_index < qrs_offset_index:
            points.append(s_point)

        if direction < 0:
            points.insert(0, qrs_offset_point)
        else:
            points.append(qrs_offset_point)

        delineation.offset_index = qrs_offset_index

    else:

        qrs_offset_index = offset_index
        qrs_offset_value = ecg_lead.filtrated[qrs_offset_index]
        qrs_offset_sign = WaveSign.none
        qrs_offset_point = Point(PointName.qrs_offset, qrs_offset_index, qrs_offset_value, qrs_offset_sign)
        if direction < 0:
            points.insert(0, qrs_offset_point)
        else:
            points.append(qrs_offset_point)


def q_r_s_processing(ecg_lead, delineation, qrs_morphology_data, q_zc_id_diff, left_points, s_zc_id_diff, right_points):

    points = []

    scale_id = qrs_morphology_data.scale_id

    r_zc_id = qrs_morphology_data.peak_zcs_ids[scale_id]
    q_zc_id = r_zc_id + q_zc_id_diff
    s_zc_id = r_zc_id + s_zc_id_diff

    if left_points:
        points = left_points + points
    q_processing(q_zc_id, ecg_lead, delineation, qrs_morphology_data, points, -1)
    qrs_morphology_data = QRSMorphologyData(ecg_lead, delineation, scale_id)

    r_zc_id = qrs_morphology_data.peak_zcs_ids[scale_id]
    q_zc_id = r_zc_id + q_zc_id_diff
    s_zc_id = r_zc_id + s_zc_id_diff

    r_processing(r_zc_id, ecg_lead, delineation, qrs_morphology_data, points, 1)
    qrs_morphology_data = QRSMorphologyData(ecg_lead, delineation, scale_id)

    r_zc_id = qrs_morphology_data.peak_zcs_ids[scale_id]
    q_zc_id = r_zc_id + q_zc_id_diff
    s_zc_id = r_zc_id + s_zc_id_diff

    if right_points:
        points = points + right_points
    s_processing(s_zc_id, ecg_lead, delineation, qrs_morphology_data, points, 1)
    qrs_morphology_data = QRSMorphologyData(ecg_lead, delineation, scale_id)

    return points


def s_r_q_processing(ecg_lead, delineation, qrs_morphology_data, q_zc_id_diff, left_points, s_zc_id_diff, right_points):

    points = []

    scale_id = qrs_morphology_data.scale_id

    r_zc_id = qrs_morphology_data.peak_zcs_ids[scale_id]
    q_zc_id = r_zc_id + q_zc_id_diff
    s_zc_id = r_zc_id + s_zc_id_diff

    if right_points:
        points = points + right_points
    s_processing(s_zc_id, ecg_lead, delineation, qrs_morphology_data, points, 1)
    qrs_morphology_data = QRSMorphologyData(ecg_lead, delineation, scale_id)

    r_zc_id = qrs_morphology_data.peak_zcs_ids[scale_id]
    q_zc_id = r_zc_id + q_zc_id_diff
    s_zc_id = r_zc_id + s_zc_id_diff

    r_processing(r_zc_id, ecg_lead, delineation, qrs_morphology_data, points, -1)
    qrs_morphology_data = QRSMorphologyData(ecg_lead, delineation, scale_id)

    r_zc_id = qrs_morphology_data.peak_zcs_ids[scale_id]
    q_zc_id = r_zc_id + q_zc_id_diff
    s_zc_id = r_zc_id + s_zc_id_diff

    if left_points:
        points = left_points + points
    q_processing(q_zc_id, ecg_lead, delineation, qrs_morphology_data, points, -1)
    qrs_morphology_data = QRSMorphologyData(ecg_lead, delineation, scale_id)

    return points


def processing_default_morphology(ecg_lead, delineation, qrs_morphology_data):

    points = []

    scale_id = qrs_morphology_data.scale_id
    zcs = qrs_morphology_data.zcs[scale_id]
    peak_zc_id = qrs_morphology_data.peak_zcs_ids[scale_id]

    onset_index = delineation.onset_index
    offset_index = delineation.offset_index

    qrs_onset_index = onset_index
    qrs_onset_value = ecg_lead.filtrated[qrs_onset_index]
    qrs_onset_sign = WaveSign.none
    qrs_onset_point = Point(PointName.qrs_onset, qrs_onset_index, qrs_onset_value, qrs_onset_sign)
    points.insert(0, qrs_onset_point)

    r_index = zcs[peak_zc_id].index
    r_value = ecg_lead.filtrated[r_index]
    if zcs[peak_zc_id].extremum_sign is ExtremumSign.negative:
        r_sign = WaveSign.negative
    else:
        r_sign = WaveSign.positive
    r_point = Point(PointName.r, r_index, r_value, r_sign)
    points.append(r_point)

    qrs_offset_index = offset_index
    qrs_offset_value = ecg_lead.filtrated[qrs_offset_index]
    qrs_offset_sign = WaveSign.none
    qrs_offset_point = Point(PointName.qrs_offset, qrs_offset_index, qrs_offset_value, qrs_offset_sign)
    points.append(qrs_offset_point)

    return points


def is_left_qrs_morphology_complex(ecg_lead, qrs_morphology_data):
    scale_id = qrs_morphology_data.scale_id
    zcs = qrs_morphology_data.zcs[scale_id]
    peak_zc_id = qrs_morphology_data.peak_zcs_ids[scale_id]

    scale_id_origin = int(QRSParams['WDC_SCALE_ID'])
    zcs_origin = qrs_morphology_data.zcs[scale_id_origin]
    peak_zc_id_origin = qrs_morphology_data.peak_zcs_ids[scale_id_origin]
    dels_zcs_ids_origin = qrs_morphology_data.dels_zcs_ids[scale_id_origin]

    peak_zc_id_origin_index = dels_zcs_ids_origin.index(peak_zc_id_origin)

    if 0 < peak_zc_id_origin_index < len(dels_zcs_ids_origin) - 1:
        dels_zcs_ids_origin = dels_zcs_ids_origin[peak_zc_id_origin_index-1:peak_zc_id_origin_index+2]
    elif 0 < peak_zc_id_origin_index == len(dels_zcs_ids_origin) - 1:
        dels_zcs_ids_origin = dels_zcs_ids_origin[peak_zc_id_origin_index-1:len(dels_zcs_ids_origin)]
    elif 0 == peak_zc_id_origin_index < len(dels_zcs_ids_origin) - 1:
        dels_zcs_ids_origin = dels_zcs_ids_origin[peak_zc_id_origin_index:peak_zc_id_origin_index+2]
    else:
        dels_zcs_ids_origin = dels_zcs_ids_origin

    original_certified_id = dels_zcs_ids_origin[0]
    if original_certified_id == peak_zc_id_origin:
        return False, None, None
    else:

        index_original_certified = zcs_origin[original_certified_id].index

        xtd_zcs_ids = []
        xtd_zc_id = peak_zc_id - 1

        while xtd_zc_id >= 0 and zcs[xtd_zc_id].index >= index_original_certified:
            xtd_zcs_ids.append(xtd_zc_id)
            xtd_zc_id -= 1

        if xtd_zc_id >= 0 and len(xtd_zcs_ids) % 2 == 0:
            dist_1 = abs(zcs[xtd_zc_id + 1].index - index_original_certified)
            dist_2 = abs(zcs[xtd_zc_id].index - index_original_certified)
            if float(dist_2) < float(QRSParams['MORPHOLOGY_SCALES_DIFF']) * float(dist_1):
                xtd_zcs_ids.append(xtd_zc_id)
            else:
                if len(xtd_zcs_ids) > 0:
                    xtd_zcs_ids.pop()

        if len(xtd_zcs_ids) <= 1:
            return False, None, None

        else:
            q_zc_id = xtd_zcs_ids[-1]
            points = []
            for xtd_point_zc_id in xtd_zcs_ids[0:-1]:
                p_index = zcs[xtd_point_zc_id].index
                p_value = ecg_lead.filtrated[p_index]
                if zcs[xtd_point_zc_id].extremum_sign is ExtremumSign.negative:
                    p_sign = WaveSign.negative
                else:
                    p_sign = WaveSign.positive
                p = Point(PointName.xtd_point, p_index, p_value, p_sign)

                points.insert(0, p)

            return True, q_zc_id, points


def is_right_qrs_morphology_complex(ecg_lead, qrs_morphology_data):
    scale_id = qrs_morphology_data.scale_id
    zcs = qrs_morphology_data.zcs[scale_id]
    peak_zc_id = qrs_morphology_data.peak_zcs_ids[scale_id]

    scale_id_origin = int(QRSParams['WDC_SCALE_ID'])
    zcs_origin = qrs_morphology_data.zcs[scale_id_origin]
    peak_zc_id_origin = qrs_morphology_data.peak_zcs_ids[scale_id_origin]
    dels_zcs_ids_origin = qrs_morphology_data.dels_zcs_ids[scale_id_origin]

    peak_zc_id_origin_index = dels_zcs_ids_origin.index(peak_zc_id_origin)

    if 0 < peak_zc_id_origin_index < len(dels_zcs_ids_origin) - 1:
        dels_zcs_ids_origin = dels_zcs_ids_origin[peak_zc_id_origin_index-1:peak_zc_id_origin_index+2]
    elif 0 < peak_zc_id_origin_index == len(dels_zcs_ids_origin) - 1:
        dels_zcs_ids_origin = dels_zcs_ids_origin[peak_zc_id_origin_index-1:len(dels_zcs_ids_origin)]
    elif 0 == peak_zc_id_origin_index < len(dels_zcs_ids_origin) - 1:
        dels_zcs_ids_origin = dels_zcs_ids_origin[peak_zc_id_origin_index:peak_zc_id_origin_index+2]
    else:
        dels_zcs_ids_origin = dels_zcs_ids_origin

    original_certified_id = dels_zcs_ids_origin[-1]
    if original_certified_id == peak_zc_id_origin:
        return False, None, None
    else:

        index_original_certified = zcs_origin[original_certified_id].index

        xtd_zcs_ids = []
        xtd_zc_id = peak_zc_id + 1

        while xtd_zc_id < len(zcs) and zcs[xtd_zc_id].index <= index_original_certified:
            xtd_zcs_ids.append(xtd_zc_id)
            xtd_zc_id += 1

        if xtd_zc_id < len(zcs) and len(xtd_zcs_ids) % 2 == 0:
            dist_1 = abs(zcs[xtd_zc_id - 1].index - index_original_certified)
            dist_2 = abs(zcs[xtd_zc_id].index - index_original_certified)
            if float(dist_2) < float(QRSParams['MORPHOLOGY_SCALES_DIFF']) * float(dist_1):
                xtd_zcs_ids.append(xtd_zc_id)
            else:
                if len(xtd_zcs_ids) > 0:
                    xtd_zcs_ids.pop()

        if len(xtd_zcs_ids) <= 1:
            return False, None, None
        else:
            s_zc_id = xtd_zcs_ids[-1]
            points = []
            for xtd_point_zc_id in xtd_zcs_ids[0:-1]:
                p_index = zcs[xtd_point_zc_id].index
                p_value = ecg_lead.filtrated[p_index]
                if zcs[xtd_point_zc_id].extremum_sign is ExtremumSign.negative:
                    p_sign = WaveSign.negative
                else:
                    p_sign = WaveSign.positive
                p = Point(PointName.xtd_point, p_index, p_value, p_sign)

                points.append(p)

            return True, s_zc_id, points
