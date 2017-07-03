from Source.Model.main.zero_crossings.zero_crossing import *
from Source.Model.main.delineation.qrs.onset import *
from Source.Model.main.delineation.qrs.offset import *
from Source.Model.main.delineation.qrs.gamma.beta_legacy import *
from Source.Model.main.params.qrs import *
from Source.Model.main.delineation.morfology_point import *


def right_qrs_morphology(ecg_lead, delineation, qrs_morphology_data):

    # Init data for target wdc scale
    scale_id = qrs_morphology_data.scale_id
    wdc = qrs_morphology_data.wdc[scale_id]
    zcs = qrs_morphology_data.zcs[scale_id]
    peak_zc_id = qrs_morphology_data.peak_zcs_ids[scale_id]
    dels_zcs_ids = qrs_morphology_data.dels_zcs_ids[scale_id]

    # Init data for original wdc scale
    scale_id_origin = int(QRSParams['WDC_SCALE_ID'])
    wdc_origin = qrs_morphology_data.wdc[scale_id_origin]
    zcs_origin = qrs_morphology_data.zcs[scale_id_origin]
    peak_zc_id_origin = qrs_morphology_data.peak_zcs_ids[scale_id_origin]
    dels_zcs_ids_origin = qrs_morphology_data.dels_zcs_ids[scale_id_origin]

    offset_index_beta = delineation.offset_index

    # Analysis of zcs count in original wdc
    dels_zcs_ids_origin = origin_scale_analysis(ecg_lead, qrs_morphology_data)

    # Init result data
    is_s_exist = False
    s_zc_id = 0
    points = []
    last_zc_id = 0

    right_zc_id_origin = dels_zcs_ids_origin[-1]

    # If there is no zc on original scale,
    # which explicit corresponds to S
    if right_zc_id_origin == peak_zc_id_origin:

        # Init left (aux) and right borders
        left_index = zcs_origin[right_zc_id_origin].index
        right_index = find_right_thc_index(wdc_origin, left_index + 1, qrs_morphology_data.end_index, 0.0)
        right_index = min(right_index, offset_index_beta)

        # Form mms array in searching interval
        mms = []
        mm_curr = find_right_mm(left_index, wdc)
        mm_next = mm_curr
        while mm_next.index < right_index:
            mm_curr = mm_next
            mms.append(mm_curr)
            mm_next = find_right_mm(mm_curr.index + 1, wdc)

        # Define list, which contains correct mms ids
        correct_mms_ids = []
        for mm_id in range(0, len(mms)):
            if mms[mm_id].correctness:
                correct_mms_ids.append(mm_id)

        # Choose last correct mm index (if exist)
        # as new right border
        if len(mms) > 0:
            if len(correct_mms_ids) > 0:
                last_correct_mm_id = correct_mms_ids[-1]
                right_index = mms[last_correct_mm_id].index

        # Creating list of additional morphology points
        xtd_zcs_ids = []
        xtd_zc_id = peak_zc_id + 1

        while xtd_zc_id < len(zcs) and zcs[xtd_zc_id].index <= right_index:
            xtd_zcs_ids.append(xtd_zc_id)
            xtd_zc_id += 1

        # If some additional points is found
        if len(xtd_zcs_ids) > 0:

            # If that list contains even count
            # (more than 0) of zcs, then there is no S
            if len(xtd_zcs_ids) % 2 == 0:
                is_s_exist = False
            # Else, there is somewhere S
            else:
                is_s_exist = True

            # If S exist, it corresponds to odd zc with bigger amplitude
            if is_s_exist:
                s_zc_id = xtd_zcs_ids[0]
                s_zc_amplitude = zcs[s_zc_id].mm_amplitude
                for zc_id in range(xtd_zcs_ids[0], xtd_zcs_ids[0] + len(xtd_zcs_ids), 2):
                    if zcs[zc_id].mm_amplitude > s_zc_amplitude:
                        s_zc_id = zc_id
                        s_zc_amplitude = zcs[s_zc_id].mm_amplitude

    # There is zc on original scale,
    # which explicit corresponds to S
    else:

        # Init left (aux) and right borders
        left_index = zcs_origin[peak_zc_id_origin].index
        right_index = offset_index_beta

        # Creating list of additional morphology points
        xtd_zcs_ids = []
        xtd_zc_id = peak_zc_id + 1

        while xtd_zc_id < len(zcs) and zcs[xtd_zc_id].index <= right_index:
            xtd_zcs_ids.append(xtd_zc_id)
            xtd_zc_id += 1

        # Some additional checking, that we really
        # found at least one zc, corresponding to S
        if len(xtd_zcs_ids) > 0:

            is_s_exist = True

            # If that list contains even count,
            # then we must consider deletion
            # of last or insertion of next
            if len(xtd_zcs_ids) % 2 == 0:
                last_xtd_zc_id = xtd_zcs_ids[-1]
                if last_xtd_zc_id < len(zcs) - 1:
                    dist_1 = abs(zcs[last_xtd_zc_id].index - right_index)
                    dist_2 = abs(zcs[last_xtd_zc_id + 1].index - right_index)
                    if float(dist_2) < float(QRSParams['MORPHOLOGY_SCALES_DIFF']) * float(dist_1):
                        xtd_zcs_ids.append(last_xtd_zc_id + 1)
                    else:
                        xtd_zcs_ids.pop()
                else:
                    xtd_zcs_ids.pop()

            # If S exist, it corresponds to odd zc with bigger amplitude
            if is_s_exist:
                s_zc_id = xtd_zcs_ids[0]
                s_zc_amplitude = zcs[s_zc_id].mm_amplitude
                for zc_id in range(xtd_zcs_ids[0], xtd_zcs_ids[0] + len(xtd_zcs_ids), 2):
                    if zcs[zc_id].mm_amplitude > s_zc_amplitude:
                        s_zc_id = zc_id
                        s_zc_amplitude = zcs[s_zc_id].mm_amplitude

    # Adding xtd points (including S)
    for xtd_point_zc_id in xtd_zcs_ids:

        if xtd_point_zc_id == s_zc_id and is_s_exist:
            s_zc_sign = qrs_morphology_data.s_signs[scale_id]
            s_index = zcs[s_zc_id].index
            s_value = ecg_lead.filtrated[s_index]
            if s_zc_sign is ExtremumSign.positive:
                s_sign = WaveSign.positive
            else:
                s_sign = WaveSign.negative
            s_point = Point(PointName.s, s_index, s_value, s_sign)
            points.append(s_point)
        else:
            p_index = zcs[xtd_point_zc_id].index
            p_value = ecg_lead.filtrated[p_index]
            if zcs[xtd_point_zc_id].extremum_sign is ExtremumSign.negative:
                p_sign = WaveSign.negative
            else:
                p_sign = WaveSign.positive
            p = Point(PointName.xtd_point, p_index, p_value, p_sign)
            points.append(p)

    if len(xtd_zcs_ids) > 0:
        last_zc_id = xtd_zcs_ids[-1]

    if len(points) <= 1:
        return False, last_zc_id, points
    else:
        return True, last_zc_id, points
