from Source.Model.main.delineation.qrs.gamma.orders import *
from Source.Model.main.delineation.qrs.gamma.default import *
from Source.Model.main.params.qrs import *


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

    if r_zc_id not in dels_zcs_ids:
        return False

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

    if r_zc_id not in dels_zcs_ids:
        return False

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

    if r_zc_id not in dels_zcs_ids:
        return False

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

    if r_zc_id not in dels_zcs_ids:
        return False

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

    if r_zc_id not in dels_zcs_ids:
        return False

    r_zc_id_index = dels_zcs_ids.index(r_zc_id)
    q_zc_id_index = r_zc_id_index + q_zc_id_diff
    s_zc_id_index = r_zc_id_index + s_zc_id_diff

    real_dels_zcs_ids = dels_zcs_ids[0:q_zc_id_index + 1] + [dels_zcs_ids[r_zc_id_index]] + dels_zcs_ids[s_zc_id_index:]
    real_r_zc_id_index = real_dels_zcs_ids.index(r_zc_id)
    real_q_zc_id_index = real_r_zc_id_index - 1
    real_s_zc_id_index = real_r_zc_id_index + 1

    mm_small_left = zcs[peak_zc_id].g_ampl * float(QRSParams['GAMMA_MM_SMALL_PART_LEFT'])

    if len(real_dels_zcs_ids) > 2 \
            and real_r_zc_id_index == len(real_dels_zcs_ids) - 1 \
            and zcs[q_zc_id].extremum_sign is q_sign \
            and zcs[r_zc_id].extremum_sign is r_sign:

        if q_zc_id - 1 >= dels_zcs_ids[0]:
            mm_left = zcs[q_zc_id - 1].l_mms[0]
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

    if r_zc_id not in dels_zcs_ids:
        return False

    r_zc_id_index = dels_zcs_ids.index(r_zc_id)
    q_zc_id_index = r_zc_id_index + q_zc_id_diff
    s_zc_id_index = r_zc_id_index + s_zc_id_diff

    real_dels_zcs_ids = dels_zcs_ids[0:q_zc_id_index + 1] + [dels_zcs_ids[r_zc_id_index]] + dels_zcs_ids[s_zc_id_index:]
    real_r_zc_id_index = real_dels_zcs_ids.index(r_zc_id)
    real_q_zc_id_index = real_r_zc_id_index - 1
    real_s_zc_id_index = real_r_zc_id_index + 1

    mm_small_left = zcs[peak_zc_id].g_ampl * float(QRSParams['GAMMA_MM_SMALL_PART_LEFT'])

    if len(real_dels_zcs_ids) > 2 \
            and real_r_zc_id_index == len(real_dels_zcs_ids) - 1 \
            and zcs[q_zc_id].extremum_sign is q_sign \
            and zcs[r_zc_id].extremum_sign is r_sign:

        if q_zc_id - 1 >= dels_zcs_ids[0]:
            mm_left = zcs[q_zc_id - 1].l_mms[0]
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

    if r_zc_id not in dels_zcs_ids:
        return False

    r_zc_id_index = dels_zcs_ids.index(r_zc_id)
    q_zc_id_index = r_zc_id_index + q_zc_id_diff
    s_zc_id_index = r_zc_id_index + s_zc_id_diff

    real_dels_zcs_ids = dels_zcs_ids[0:q_zc_id_index + 1] + [dels_zcs_ids[r_zc_id_index]] + dels_zcs_ids[s_zc_id_index:]
    real_r_zc_id_index = real_dels_zcs_ids.index(r_zc_id)
    real_q_zc_id_index = real_r_zc_id_index - 1
    real_s_zc_id_index = real_r_zc_id_index + 1

    mm_small_left = zcs[peak_zc_id].g_ampl * float(QRSParams['GAMMA_MM_SMALL_PART_LEFT'])

    if len(real_dels_zcs_ids) > 3 \
            and real_r_zc_id_index == len(real_dels_zcs_ids) - 2 \
            and zcs[q_zc_id].extremum_sign is q_sign \
            and zcs[r_zc_id].extremum_sign is r_sign \
            and zcs[s_zc_id].extremum_sign is s_sign:

        if q_zc_id - 1 >= dels_zcs_ids[0]:
            mm_left = zcs[q_zc_id - 1].l_mms[0]
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

    if r_zc_id not in dels_zcs_ids:
        return False

    r_zc_id_index = dels_zcs_ids.index(r_zc_id)
    q_zc_id_index = r_zc_id_index + q_zc_id_diff
    s_zc_id_index = r_zc_id_index + s_zc_id_diff

    real_dels_zcs_ids = dels_zcs_ids[0:q_zc_id_index + 1] + [dels_zcs_ids[r_zc_id_index]] + dels_zcs_ids[s_zc_id_index:]
    real_r_zc_id_index = real_dels_zcs_ids.index(r_zc_id)
    real_q_zc_id_index = real_r_zc_id_index - 1
    real_s_zc_id_index = real_r_zc_id_index + 1

    mm_small_left = zcs[peak_zc_id].g_ampl * float(QRSParams['GAMMA_MM_SMALL_PART_LEFT'])

    if len(real_dels_zcs_ids) > 3 \
            and real_r_zc_id_index == len(real_dels_zcs_ids) - 2 \
            and zcs[q_zc_id].extremum_sign is q_sign \
            and zcs[r_zc_id].extremum_sign is r_sign \
            and zcs[s_zc_id].extremum_sign is s_sign:

        if q_zc_id - 1 >= dels_zcs_ids[0]:
            mm_left = zcs[q_zc_id - 1].l_mms[0]
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

    if r_zc_id not in dels_zcs_ids:
        return False

    r_zc_id_index = dels_zcs_ids.index(r_zc_id)
    q_zc_id_index = r_zc_id_index + q_zc_id_diff
    s_zc_id_index = r_zc_id_index + s_zc_id_diff

    real_dels_zcs_ids = dels_zcs_ids[0:q_zc_id_index + 1] + [dels_zcs_ids[r_zc_id_index]] + dels_zcs_ids[s_zc_id_index:]
    real_r_zc_id_index = real_dels_zcs_ids.index(r_zc_id)
    real_q_zc_id_index = real_r_zc_id_index - 1
    real_s_zc_id_index = real_r_zc_id_index + 1

    mm_small_right = zcs[peak_zc_id].g_ampl * float(QRSParams['GAMMA_MM_SMALL_PART_RIGHT'])

    if len(real_dels_zcs_ids) > 2 \
            and real_r_zc_id_index == 0 \
            and zcs[r_zc_id].extremum_sign is r_sign \
            and zcs[s_zc_id].extremum_sign is s_sign:

        if s_zc_id + 1 < dels_zcs_ids[0] + len(dels_zcs_ids):
            mm_right = zcs[s_zc_id + 1].r_mms[0]
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

    if r_zc_id not in dels_zcs_ids:
        return False

    r_zc_id_index = dels_zcs_ids.index(r_zc_id)
    q_zc_id_index = r_zc_id_index + q_zc_id_diff
    s_zc_id_index = r_zc_id_index + s_zc_id_diff

    real_dels_zcs_ids = dels_zcs_ids[0:q_zc_id_index + 1] + [dels_zcs_ids[r_zc_id_index]] + dels_zcs_ids[s_zc_id_index:]
    real_r_zc_id_index = real_dels_zcs_ids.index(r_zc_id)
    real_q_zc_id_index = real_r_zc_id_index - 1
    real_s_zc_id_index = real_r_zc_id_index + 1

    mm_small_right = zcs[peak_zc_id].g_ampl * float(QRSParams['GAMMA_MM_SMALL_PART_RIGHT'])

    if len(real_dels_zcs_ids) > 2 \
            and real_r_zc_id_index == 0 \
            and zcs[r_zc_id].extremum_sign is r_sign \
            and zcs[s_zc_id].extremum_sign is s_sign:

        if s_zc_id + 1 < dels_zcs_ids[0] + len(dels_zcs_ids):
            mm_right = zcs[s_zc_id + 1].r_mms[0]
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

    if r_zc_id not in dels_zcs_ids:
        return False

    r_zc_id_index = dels_zcs_ids.index(r_zc_id)
    q_zc_id_index = r_zc_id_index + q_zc_id_diff
    s_zc_id_index = r_zc_id_index + s_zc_id_diff

    real_dels_zcs_ids = dels_zcs_ids[0:q_zc_id_index + 1] + [dels_zcs_ids[r_zc_id_index]] + dels_zcs_ids[s_zc_id_index:]
    real_r_zc_id_index = real_dels_zcs_ids.index(r_zc_id)
    real_q_zc_id_index = real_r_zc_id_index - 1
    real_s_zc_id_index = real_r_zc_id_index + 1

    mm_small_right = zcs[peak_zc_id].g_ampl * float(QRSParams['GAMMA_MM_SMALL_PART_RIGHT'])

    if len(real_dels_zcs_ids) > 3 \
            and real_r_zc_id_index == 1 \
            and zcs[q_zc_id].extremum_sign is q_sign \
            and zcs[r_zc_id].extremum_sign is r_sign \
            and zcs[s_zc_id].extremum_sign is s_sign:

        if s_zc_id + 1 < dels_zcs_ids[0] + len(dels_zcs_ids):
            mm_right = zcs[s_zc_id + 1].r_mms[0]
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

    if r_zc_id not in dels_zcs_ids:
        return False

    r_zc_id_index = dels_zcs_ids.index(r_zc_id)
    q_zc_id_index = r_zc_id_index + q_zc_id_diff
    s_zc_id_index = r_zc_id_index + s_zc_id_diff

    real_dels_zcs_ids = dels_zcs_ids[0:q_zc_id_index + 1] + [dels_zcs_ids[r_zc_id_index]] + dels_zcs_ids[s_zc_id_index:]
    real_r_zc_id_index = real_dels_zcs_ids.index(r_zc_id)
    real_q_zc_id_index = real_r_zc_id_index - 1
    real_s_zc_id_index = real_r_zc_id_index + 1

    mm_small_right = zcs[peak_zc_id].g_ampl * float(QRSParams['GAMMA_MM_SMALL_PART_RIGHT'])

    if len(real_dels_zcs_ids) > 3 \
            and real_r_zc_id_index == 1 \
            and zcs[q_zc_id].extremum_sign is q_sign \
            and zcs[r_zc_id].extremum_sign is r_sign \
            and zcs[s_zc_id].extremum_sign is s_sign:

        if s_zc_id + 1 < dels_zcs_ids[0] + len(dels_zcs_ids):
            mm_right = zcs[s_zc_id + 1].r_mms[0]
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

    if r_zc_id not in dels_zcs_ids:
        return False

    r_zc_id_index = dels_zcs_ids.index(r_zc_id)
    q_zc_id_index = r_zc_id_index + q_zc_id_diff
    s_zc_id_index = r_zc_id_index + s_zc_id_diff

    real_dels_zcs_ids = dels_zcs_ids[0:q_zc_id_index + 1] + [dels_zcs_ids[r_zc_id_index]] + dels_zcs_ids[s_zc_id_index:]
    real_r_zc_id_index = real_dels_zcs_ids.index(r_zc_id)
    real_q_zc_id_index = real_r_zc_id_index - 1
    real_s_zc_id_index = real_r_zc_id_index + 1

    mm_small_left = zcs[peak_zc_id].g_ampl * float(QRSParams['GAMMA_MM_SMALL_PART_LEFT'])
    mm_small_right = zcs[peak_zc_id].g_ampl * float(QRSParams['GAMMA_MM_SMALL_PART_RIGHT'])

    if len(real_dels_zcs_ids) > 4 \
            and 2 <= real_r_zc_id_index < len(real_dels_zcs_ids) - 2 \
            and zcs[q_zc_id].extremum_sign is q_sign \
            and zcs[r_zc_id].extremum_sign is r_sign \
            and zcs[s_zc_id].extremum_sign is s_sign:

        if q_zc_id - 1 >= dels_zcs_ids[0] and s_zc_id + 1 < dels_zcs_ids[0] + len(dels_zcs_ids):
            mm_left = zcs[q_zc_id - 1].l_mms[0]
            mm_right = zcs[s_zc_id + 1].r_mms[0]
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

    if r_zc_id not in dels_zcs_ids:
        return False

    r_zc_id_index = dels_zcs_ids.index(r_zc_id)
    q_zc_id_index = r_zc_id_index + q_zc_id_diff
    s_zc_id_index = r_zc_id_index + s_zc_id_diff

    real_dels_zcs_ids = dels_zcs_ids[0:q_zc_id_index + 1] + [dels_zcs_ids[r_zc_id_index]] + dels_zcs_ids[s_zc_id_index:]
    real_r_zc_id_index = real_dels_zcs_ids.index(r_zc_id)
    real_q_zc_id_index = real_r_zc_id_index - 1
    real_s_zc_id_index = real_r_zc_id_index + 1

    mm_small_left = zcs[peak_zc_id].g_ampl * float(QRSParams['GAMMA_MM_SMALL_PART_LEFT'])
    mm_small_right = zcs[peak_zc_id].g_ampl * float(QRSParams['GAMMA_MM_SMALL_PART_RIGHT'])

    if len(real_dels_zcs_ids) > 4 \
            and 2 <= real_r_zc_id_index < len(real_dels_zcs_ids) - 2 \
            and zcs[q_zc_id].extremum_sign is q_sign \
            and zcs[r_zc_id].extremum_sign is r_sign \
            and zcs[s_zc_id].extremum_sign is s_sign:

        if q_zc_id - 1 >= dels_zcs_ids[0] and s_zc_id + 1 < dels_zcs_ids[0] + len(dels_zcs_ids):
            mm_left = zcs[q_zc_id - 1].l_mms[0]
            mm_right = zcs[s_zc_id + 1].r_mms[0]
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

    if r_zc_id not in dels_zcs_ids:
        return False

    r_zc_id_index = dels_zcs_ids.index(r_zc_id)
    q_zc_id_index = r_zc_id_index + q_zc_id_diff
    s_zc_id_index = r_zc_id_index + s_zc_id_diff

    real_dels_zcs_ids = dels_zcs_ids[0:q_zc_id_index + 1] + [dels_zcs_ids[r_zc_id_index]] + dels_zcs_ids[s_zc_id_index:]
    real_r_zc_id_index = real_dels_zcs_ids.index(r_zc_id)
    real_q_zc_id_index = real_r_zc_id_index - 1
    real_s_zc_id_index = real_r_zc_id_index + 1

    mm_small_left = zcs[peak_zc_id].g_ampl * float(QRSParams['GAMMA_MM_SMALL_PART_LEFT'])
    mm_small_right = zcs[peak_zc_id].g_ampl * float(QRSParams['GAMMA_MM_SMALL_PART_RIGHT'])

    if len(real_dels_zcs_ids) > 4 \
            and 2 <= real_r_zc_id_index < len(real_dels_zcs_ids) - 2 \
            and zcs[q_zc_id].extremum_sign is q_sign \
            and zcs[r_zc_id].extremum_sign is r_sign \
            and zcs[s_zc_id].extremum_sign is s_sign:

        if q_zc_id - 1 >= dels_zcs_ids[0] and s_zc_id + 1 < dels_zcs_ids[0] + len(dels_zcs_ids):
            mm_left = zcs[q_zc_id - 1].l_mms[0]
            mm_right = zcs[s_zc_id + 1].r_mms[0]
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

    if r_zc_id not in dels_zcs_ids:
        return False

    r_zc_id_index = dels_zcs_ids.index(r_zc_id)
    q_zc_id_index = r_zc_id_index + q_zc_id_diff
    s_zc_id_index = r_zc_id_index + s_zc_id_diff

    real_dels_zcs_ids = dels_zcs_ids[0:q_zc_id_index + 1] + [dels_zcs_ids[r_zc_id_index]] + dels_zcs_ids[s_zc_id_index:]
    real_r_zc_id_index = real_dels_zcs_ids.index(r_zc_id)
    real_q_zc_id_index = real_r_zc_id_index - 1
    real_s_zc_id_index = real_r_zc_id_index + 1

    mm_small_left = zcs[peak_zc_id].g_ampl * float(QRSParams['GAMMA_MM_SMALL_PART_LEFT'])
    mm_small_right = zcs[peak_zc_id].g_ampl * float(QRSParams['GAMMA_MM_SMALL_PART_RIGHT'])

    if len(real_dels_zcs_ids) > 4 \
            and 2 <= real_r_zc_id_index < len(real_dels_zcs_ids) - 2 \
            and zcs[q_zc_id].extremum_sign is q_sign \
            and zcs[r_zc_id].extremum_sign is r_sign \
            and zcs[s_zc_id].extremum_sign is s_sign:

        if q_zc_id - 1 >= dels_zcs_ids[0] and s_zc_id + 1 < dels_zcs_ids[0] + len(dels_zcs_ids):
            mm_left = zcs[q_zc_id - 1].l_mms[0]
            mm_right = zcs[s_zc_id + 1].r_mms[0]
            if abs(mm_left.value) > mm_small_left and abs(mm_right.value) > mm_small_right:
                return True

    else:
        return False
