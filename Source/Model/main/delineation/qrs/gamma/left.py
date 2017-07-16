from Source.Model.main.delineation.qrs.onset import *
from Source.Model.main.delineation.qrs.offset import *
from Source.Model.main.delineation.qrs.gamma.beta_legacy import *
from Source.Model.main.params.qrs import *
from Source.Model.main.delineation.morfology_point import *


def left_qrs_morphology(ecg_lead, delineation, qrs_morphology_data):

    sampling_rate = ecg_lead.sampling_rate

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

    onset_index_beta = delineation.onset_index

    # Analysis of zcs count in original wdc
    dels_zcs_ids_origin = origin_scale_analysis(ecg_lead, qrs_morphology_data)

    # Init result data
    is_q_exist = False
    q_zc_id = 0
    points = []
    first_zc_id = 0

    left_zc_id_origin = dels_zcs_ids_origin[0]

    # If there is no zc on original scale,
    # which explicit corresponds to Q
    if left_zc_id_origin == peak_zc_id_origin:

        # Init left and right (aux) borders
        right_index = zcs_origin[left_zc_id_origin].index
        left_index = find_left_thc_index(wdc_origin, right_index - 1, qrs_morphology_data.begin_index, 0.0)
        left_index = max(left_index, onset_index_beta)

        # Form mms array in searching interval
        mms = []
        mm_curr = find_left_mm(right_index, wdc)
        mm_next = mm_curr
        while mm_next.index > left_index:
            mm_curr = mm_next
            mms.append(mm_curr)
            mm_next = find_left_mm(mm_curr.index - 1, wdc)

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
                left_index = mms[last_correct_mm_id].index

        # Creating list of additional morphology points
        xtd_zcs_ids = []
        xtd_zc_id = peak_zc_id - 1

        while xtd_zc_id >= 0 and zcs[xtd_zc_id].index >= left_index:
            xtd_zcs_ids.append(xtd_zc_id)
            xtd_zc_id -= 1

        # If some additional points is found
        if len(xtd_zcs_ids) > 0:

            # If that list contains even count
            # (more than 0) of zcs, then there is no Q
            if len(xtd_zcs_ids) % 2 == 0:
                is_q_exist = False
            # Else, there is somewhere S
            else:
                is_q_exist = True

            # If Q exist, it corresponds to odd zc with bigger amplitude
            if is_q_exist:
                q_zc_id = xtd_zcs_ids[0]
                q_zc_amplitude = zcs[q_zc_id].mm_amplitude
                for zc_id in range(xtd_zcs_ids[0], xtd_zcs_ids[0] - len(xtd_zcs_ids), -2):
                    if zcs[zc_id].mm_amplitude > q_zc_amplitude:
                        q_zc_id = zc_id
                        q_zc_amplitude = zcs[q_zc_id].mm_amplitude

    # There is zc on original scale,
    # which explicit corresponds to Q
    else:

        # Init left (aux) and right borders
        right_index = zcs_origin[peak_zc_id_origin].index
        left_index = onset_index_beta

        # Creating list of additional morphology points
        xtd_zcs_ids = []
        xtd_zc_id = peak_zc_id - 1

        while xtd_zc_id >= 0 and zcs[xtd_zc_id].index >= left_index:
            xtd_zcs_ids.append(xtd_zc_id)
            xtd_zc_id -= 1

        # Some additional checking, that we really
        # found at least one zc, corresponding to Q
        if len(xtd_zcs_ids) > 0:

            is_q_exist = True

            # If that list contains even count,
            # then we must consider deletion
            # of last or insertion of next
            if len(xtd_zcs_ids) % 2 == 0:
                first_xtd_zc_id = xtd_zcs_ids[-1]
                if first_xtd_zc_id > 0:
                    dist_1 = abs(zcs[first_xtd_zc_id].index - right_index)
                    dist_2 = abs(zcs[first_xtd_zc_id - 1].index - right_index)
                    if float(dist_2) < float(QRSParams['MORPHOLOGY_SCALES_DIFF']) * float(dist_1):
                        xtd_zcs_ids.append(first_xtd_zc_id - 1)
                    else:
                        xtd_zcs_ids.pop()
                else:
                    xtd_zcs_ids.pop()

            # If Q exist, it corresponds to odd zc with bigger amplitude
            # If there is zcs after Q-zc we should check them
            if is_q_exist:
                q_zc_id = xtd_zcs_ids[0]
                q_zc_amplitude = zcs[q_zc_id].mm_amplitude
                for zc_id in range(xtd_zcs_ids[0], xtd_zcs_ids[0] - len(xtd_zcs_ids), -2):
                    if zcs[zc_id].mm_amplitude > q_zc_amplitude:
                        q_zc_id = zc_id
                        q_zc_amplitude = zcs[q_zc_id].mm_amplitude

                # Check zcs after Q-zc
                if xtd_zcs_ids[-1] < q_zc_id:
                    after_q_zcs_ids = xtd_zcs_ids[xtd_zcs_ids.index(q_zc_id) + 1:]
                    if len(after_q_zcs_ids) % 2 == 1:
                        after_q_zcs_ids.pop()

                    is_zcs_valid = True
                    zc_shift = int(float(QRSParams['GAMMA_XTD_ZCS_SHIFT']) * sampling_rate)
                    for zc_id in after_q_zcs_ids[0:-1:2]:
                        if abs(zcs[zc_id].index - zcs[zc_id + 1].index) > zc_shift:
                            is_zcs_valid = False

                    if is_zcs_valid:
                        if len(after_q_zcs_ids) > 0:
                            xtd_zcs_ids = xtd_zcs_ids[0:xtd_zcs_ids.index(q_zc_id) + 1] + after_q_zcs_ids
                    else:
                        xtd_zcs_ids = xtd_zcs_ids[0:xtd_zcs_ids.index(q_zc_id) + 1]

    # Adding xtd points (including Q)
    for xtd_point_zc_id in xtd_zcs_ids:

        if xtd_point_zc_id == q_zc_id and is_q_exist:
            q_zc_sign = qrs_morphology_data.q_signs[scale_id]
            q_index = zcs[q_zc_id].index
            q_value = ecg_lead.filtrated[q_index]
            if q_zc_sign is ExtremumSign.positive:
                q_sign = WaveSign.positive
            else:
                q_sign = WaveSign.negative
            q_point = Point(PointName.q, q_index, q_value, q_sign)
            points.insert(0, q_point)
        else:
            p_index = zcs[xtd_point_zc_id].index
            p_value = ecg_lead.filtrated[p_index]
            if zcs[xtd_point_zc_id].extremum_sign is ExtremumSign.negative:
                p_sign = WaveSign.negative
            else:
                p_sign = WaveSign.positive
            p = Point(PointName.xtd_point, p_index, p_value, p_sign)
            points.insert(0, p)

    if len(xtd_zcs_ids) > 0:
        first_zc_id = xtd_zcs_ids[-1]

    if len(points) <= 1:
        return False, first_zc_id, points
    else:
        return True, first_zc_id, points
