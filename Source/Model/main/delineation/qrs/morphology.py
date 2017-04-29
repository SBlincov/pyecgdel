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

            dels_zcs_ids.append(current_dels_zcs_ids)
            peak_zcs_ids.append(peak_zc_id)

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


def get_qrs_morphology(ecg_lead, del_id, delineation):
    points = []

    scale_id = 0

    qrs_morphology_data = QRSMorphologyData(ecg_lead, delineation, scale_id)

    if is_r_pos_in_del(qrs_morphology_data):
        # Branch #1:
        branch_id = 1
        r_pos_in_del_processing(ecg_lead, delineation, qrs_morphology_data, points)

    elif is_q_neg_r_pos_in_del(qrs_morphology_data):
        # Branch #2:
        branch_id = 2
        q_neg_r_pos_in_del_processing(ecg_lead, delineation, qrs_morphology_data, points)

    elif is_r_pos_s_neg_in_del(qrs_morphology_data):
        # Branch #3:
        branch_id = 3
        r_pos_s_neg_in_del_processing(ecg_lead, delineation, qrs_morphology_data, points)

    elif is_q_neg_r_pos_s_neg_in_del(qrs_morphology_data):
        # Branch #4:
        branch_id = 4
        q_neg_r_pos_s_neg_in_del_processing(ecg_lead, delineation, qrs_morphology_data, points)

    else:
        # Default:
        # Branch #0
        branch_id = 0
        processing_default_morphology(ecg_lead, delineation, qrs_morphology_data, points)

    morphology = Morphology(del_id, points, branch_id)

    return morphology


def is_r_pos_in_del(qrs_morphology_data):
    scale_id = qrs_morphology_data.scale_id
    zcs = qrs_morphology_data.zcs[scale_id]
    dels_zcs_ids = qrs_morphology_data.dels_zcs_ids[scale_id]
    peak_zc_id = qrs_morphology_data.peak_zcs_ids[scale_id]

    if len(dels_zcs_ids) is 1 \
            and peak_zc_id == dels_zcs_ids[0] \
            and zcs[dels_zcs_ids[0]].extremum_sign is ExtremumSign.positive:
        return True
    else:
        return False


def is_q_neg_r_pos_in_del(qrs_morphology_data):
    scale_id = qrs_morphology_data.scale_id
    zcs = qrs_morphology_data.zcs[scale_id]
    dels_zcs_ids = qrs_morphology_data.dels_zcs_ids[scale_id]
    peak_zc_id = qrs_morphology_data.peak_zcs_ids[scale_id]

    if len(dels_zcs_ids) is 2 \
            and peak_zc_id == dels_zcs_ids[1] \
            and zcs[dels_zcs_ids[0]].extremum_sign is ExtremumSign.negative \
            and zcs[dels_zcs_ids[1]].extremum_sign is ExtremumSign.positive:
        return True
    else:
        return False


def is_r_pos_s_neg_in_del(qrs_morphology_data):
    scale_id = qrs_morphology_data.scale_id
    zcs = qrs_morphology_data.zcs[scale_id]
    dels_zcs_ids = qrs_morphology_data.dels_zcs_ids[scale_id]
    peak_zc_id = qrs_morphology_data.peak_zcs_ids[scale_id]

    if len(dels_zcs_ids) is 2 \
            and peak_zc_id == dels_zcs_ids[0] \
            and zcs[dels_zcs_ids[0]].extremum_sign is ExtremumSign.positive \
            and zcs[dels_zcs_ids[1]].extremum_sign is ExtremumSign.negative:
        return True
    else:
        return False


def is_q_neg_r_pos_s_neg_in_del(qrs_morphology_data):
    scale_id = qrs_morphology_data.scale_id
    zcs = qrs_morphology_data.zcs[scale_id]
    dels_zcs_ids = qrs_morphology_data.dels_zcs_ids[scale_id]
    peak_zc_id = qrs_morphology_data.peak_zcs_ids[scale_id]

    if len(dels_zcs_ids) is 3 \
            and peak_zc_id == dels_zcs_ids[0] \
            and zcs[dels_zcs_ids[0]].extremum_sign is ExtremumSign.negative \
            and zcs[dels_zcs_ids[1]].extremum_sign is ExtremumSign.positive \
            and zcs[dels_zcs_ids[2]].extremum_sign is ExtremumSign.negative:
        return True
    else:
        return False


def q_neg_processing(q_zc_id, ecg_lead, delineation, qrs_morphology_data, points, direction):
    scale_id = qrs_morphology_data.scale_id
    wdc = qrs_morphology_data.wdc[scale_id]
    zcs = qrs_morphology_data.zcs[scale_id]
    begin_index = qrs_morphology_data.begin_index

    onset_index = delineation.onset_index

    if q_zc_id >= 0 and zcs[q_zc_id].extremum_sign is ExtremumSign.negative:

        q_index = zcs[q_zc_id].index
        q_value = ecg_lead.filtrated[q_index]
        q_sign = WaveSign.negative
        q_point = Point(PointName.q, q_index, q_value, q_sign)
        points.insert(0, q_point)

        mm_curr = find_left_mm(q_index, wdc)
        mm_next = mm_curr
        mms = []
        # While mms have the same sign and take place in allowed interval
        while mm_curr.value * mm_next.value > 0 and mm_curr.index > begin_index:
            mm_curr = mm_next
            mms.append(mm_curr)
            mm_next = find_left_mm(mm_curr.index - 1, wdc)

        qrs_onset_index = begin_index

        if mms:
            mm_onset = mms[0]
            if len(mms) > 1:
                # Simple way: the second mm in mms is incorrect
                mm_onset = mms[1]

            if mm_onset.index > qrs_onset_index:
                qrs_onset_index = mm_onset.index

        qrs_onset_value = ecg_lead.filtrated[qrs_onset_index]
        qrs_onset_sign = WaveSign.none
        qrs_onset_point = Point(PointName.qrs_onset, qrs_onset_index, qrs_onset_value, qrs_onset_sign)
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


def r_pos_processing(r_zc_id, ecg_lead, delineation, qrs_morphology_data, points, direction):
    scale_id = qrs_morphology_data.scale_id
    zcs = qrs_morphology_data.zcs[scale_id]

    r_index = zcs[r_zc_id].index
    r_value = ecg_lead.filtrated[r_index]
    r_sign = WaveSign.positive
    r_point = Point(PointName.r, r_index, r_value, r_sign)
    if direction < 0:
        points.insert(0, r_point)
    else:
        points.append(r_point)

    delineation.peak_index = r_index


def s_neg_processing(s_zc_id, ecg_lead, delineation, qrs_morphology_data, points, direction):
    scale_id = qrs_morphology_data.scale_id
    wdc = qrs_morphology_data.wdc[scale_id]
    zcs = qrs_morphology_data.zcs[scale_id]
    end_index = qrs_morphology_data.end_index

    offset_index = delineation.offset_index

    if s_zc_id < len(zcs) and zcs[s_zc_id].extremum_sign is ExtremumSign.negative:

        s_index = zcs[s_zc_id].index
        s_value = ecg_lead.filtrated[s_index]
        s_sign = WaveSign.negative
        s_point = Point(PointName.s, s_index, s_value, s_sign)
        points.append(s_point)

        mm_curr = find_right_mm(s_index, wdc)
        mm_next = mm_curr
        mms = []
        # While mms have the same sign and take place in allowed interval
        while mm_curr.value * mm_next.value > 0 and mm_curr.index < end_index:
            mm_curr = mm_next
            mms.append(mm_curr)
            mm_next = find_right_mm(mm_curr.index + 1, wdc)

        qrs_offset_index = end_index

        if mms:
            mm_offset = mms[0]
            if len(mms) > 1:
                # Simple way: the second mm in mms is incorrect
                mm_offset = mms[1]

            if mm_offset.index < qrs_offset_index:
                qrs_offset_index = mm_offset.index

        qrs_offset_value = ecg_lead.filtrated[qrs_offset_index]
        qrs_offset_sign = WaveSign.none
        qrs_offset_point = Point(PointName.qrs_offset, qrs_offset_index, qrs_offset_value, qrs_offset_sign)
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


def r_pos_in_del_processing(ecg_lead, delineation, qrs_morphology_data, points):
    scale_id = qrs_morphology_data.scale_id
    peak_zc_id = qrs_morphology_data.peak_zcs_ids[scale_id]
    r_zc_id = peak_zc_id
    q_zc_id = r_zc_id - 1
    s_zc_id = r_zc_id + 1

    q_neg_processing(q_zc_id, ecg_lead, delineation, qrs_morphology_data, points, -1)
    qrs_morphology_data = QRSMorphologyData(ecg_lead, delineation, scale_id)

    scale_id = qrs_morphology_data.scale_id
    peak_zc_id = qrs_morphology_data.peak_zcs_ids[scale_id]
    r_zc_id = peak_zc_id
    q_zc_id = r_zc_id - 1
    s_zc_id = r_zc_id + 1

    r_pos_processing(r_zc_id, ecg_lead, delineation, qrs_morphology_data, points, 1)
    qrs_morphology_data = QRSMorphologyData(ecg_lead, delineation, scale_id)

    scale_id = qrs_morphology_data.scale_id
    peak_zc_id = qrs_morphology_data.peak_zcs_ids[scale_id]
    r_zc_id = peak_zc_id
    q_zc_id = r_zc_id - 1
    s_zc_id = r_zc_id + 1

    s_neg_processing(s_zc_id, ecg_lead, delineation, qrs_morphology_data, points, 1)
    qrs_morphology_data = QRSMorphologyData(ecg_lead, delineation, scale_id)


def q_neg_r_pos_in_del_processing(ecg_lead, delineation, qrs_morphology_data, points):
    scale_id = qrs_morphology_data.scale_id
    peak_zc_id = qrs_morphology_data.peak_zcs_ids[scale_id]
    r_zc_id = peak_zc_id
    q_zc_id = r_zc_id - 1
    s_zc_id = r_zc_id + 1

    q_neg_processing(q_zc_id, ecg_lead, delineation, qrs_morphology_data, points, -1)
    qrs_morphology_data = QRSMorphologyData(ecg_lead, delineation, scale_id)

    scale_id = qrs_morphology_data.scale_id
    peak_zc_id = qrs_morphology_data.peak_zcs_ids[scale_id]
    r_zc_id = peak_zc_id
    q_zc_id = r_zc_id - 1
    s_zc_id = r_zc_id + 1

    r_pos_processing(r_zc_id, ecg_lead, delineation, qrs_morphology_data, points, 1)
    qrs_morphology_data = QRSMorphologyData(ecg_lead, delineation, scale_id)

    scale_id = qrs_morphology_data.scale_id
    peak_zc_id = qrs_morphology_data.peak_zcs_ids[scale_id]
    r_zc_id = peak_zc_id
    q_zc_id = r_zc_id - 1
    s_zc_id = r_zc_id + 1

    s_neg_processing(s_zc_id, ecg_lead, delineation, qrs_morphology_data, points, 1)
    qrs_morphology_data = QRSMorphologyData(ecg_lead, delineation, scale_id)


def r_pos_s_neg_in_del_processing(ecg_lead, delineation, qrs_morphology_data, points):
    scale_id = qrs_morphology_data.scale_id
    peak_zc_id = qrs_morphology_data.peak_zcs_ids[scale_id]
    r_zc_id = peak_zc_id
    q_zc_id = r_zc_id - 1
    s_zc_id = r_zc_id + 1

    s_neg_processing(s_zc_id, ecg_lead, delineation, qrs_morphology_data, points, 1)
    qrs_morphology_data = QRSMorphologyData(ecg_lead, delineation, scale_id)

    scale_id = qrs_morphology_data.scale_id
    peak_zc_id = qrs_morphology_data.peak_zcs_ids[scale_id]
    r_zc_id = peak_zc_id
    q_zc_id = r_zc_id - 1
    s_zc_id = r_zc_id + 1

    r_pos_processing(r_zc_id, ecg_lead, delineation, qrs_morphology_data, points, -1)
    qrs_morphology_data = QRSMorphologyData(ecg_lead, delineation, scale_id)

    scale_id = qrs_morphology_data.scale_id
    peak_zc_id = qrs_morphology_data.peak_zcs_ids[scale_id]
    r_zc_id = peak_zc_id
    q_zc_id = r_zc_id - 1
    s_zc_id = r_zc_id + 1

    q_neg_processing(q_zc_id, ecg_lead, delineation, qrs_morphology_data, points, -1)
    qrs_morphology_data = QRSMorphologyData(ecg_lead, delineation, scale_id)


def q_neg_r_pos_s_neg_in_del_processing(ecg_lead, delineation, qrs_morphology_data, points):
    scale_id = qrs_morphology_data.scale_id
    peak_zc_id = qrs_morphology_data.peak_zcs_ids[scale_id]
    r_zc_id = peak_zc_id
    q_zc_id = r_zc_id - 1
    s_zc_id = r_zc_id + 1

    q_neg_processing(q_zc_id, ecg_lead, delineation, qrs_morphology_data, points, -1)
    qrs_morphology_data = QRSMorphologyData(ecg_lead, delineation, scale_id)

    scale_id = qrs_morphology_data.scale_id
    peak_zc_id = qrs_morphology_data.peak_zcs_ids[scale_id]
    r_zc_id = peak_zc_id
    q_zc_id = r_zc_id - 1
    s_zc_id = r_zc_id + 1

    r_pos_processing(r_zc_id, ecg_lead, delineation, qrs_morphology_data, points, 1)
    qrs_morphology_data = QRSMorphologyData(ecg_lead, delineation, scale_id)

    scale_id = qrs_morphology_data.scale_id
    peak_zc_id = qrs_morphology_data.peak_zcs_ids[scale_id]
    r_zc_id = peak_zc_id
    q_zc_id = r_zc_id - 1
    s_zc_id = r_zc_id + 1

    s_neg_processing(s_zc_id, ecg_lead, delineation, qrs_morphology_data, points, 1)
    qrs_morphology_data = QRSMorphologyData(ecg_lead, delineation, scale_id)


def processing_default_morphology(ecg_lead, delineation, qrs_morphology_data, points):
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
