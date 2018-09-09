from Source.Model.main.delineation.morfology_point import *
from Source.Model.main.delineation.qrs.beta.offset import *
from Source.Model.main.delineation.qrs.gamma.beta_legacy import *
from Source.Model.main.params.qrs import *
from Source.Model.main.zero_crossings.zero_crossing import *


def right_qrs_morphology(ecg_lead, delineation, morph_data):
    rate = ecg_lead.rate

    # Init data for target wdc scale
    scale_id = morph_data.scale_id
    wdc = morph_data.wdc[scale_id]
    zcs = morph_data.zcs[scale_id]
    peak_zc_id = morph_data.peak_zcs_ids[scale_id]
    zcs_all = ecg_lead.zcs[scale_id]

    # Init data for original wdc scale
    scale_id_origin = int(QRSParams['WDC_SCALE_ID'])
    wdc_origin = morph_data.wdc[scale_id_origin]
    zcs_origin = morph_data.zcs[scale_id_origin]
    peak_zc_id_origin = morph_data.peak_zcs_ids[scale_id_origin]
    zcs_all_origin = ecg_lead.zcs[scale_id_origin]

    offset_index_beta = delineation.offset_index

    # Analysis of zcs count in original wdc
    dels_zcs_ids_origin = origin_scale_analysis(ecg_lead, morph_data)

    # Init result data
    is_s_exist = False
    s_zc_id = 0
    points = []
    last_zc_id = 0

    right_zc_id_origin = dels_zcs_ids_origin[-1]
    right_zc_origin = zcs_origin[right_zc_id_origin]
    # If there is no zc on original scale,
    # which explicit corresponds to S
    if right_zc_id_origin == peak_zc_id_origin:

        # Init left border
        left_index = right_zc_origin.index

        # Init right border
        r_ind_1 = min(zcs_all_origin[right_zc_origin.id + 1].index, morph_data.end_index)
        mms_origin = get_lr_mms_in(ecg_lead, scale_id_origin, left_index, offset_index_beta)
        incorrect_mms_ids_origin = get_incorrect_mms_ids(mms_origin)
        incorrect_mm_limit = zcs_origin[peak_zc_id_origin].g_ampl * float(QRSParams['GAMMA_RIGHT_ORIGIN_INCORRECT'])
        r_ind_2 = r_ind_1
        for mm_id in incorrect_mms_ids_origin:
            if mms_origin[mm_id].value < incorrect_mm_limit:
                r_ind_2 = mms_origin[mm_id].index
                break
        right_index = min(r_ind_1, r_ind_2, offset_index_beta)

        # Form mms array in searching interval
        mms = get_lr_mms_in(ecg_lead, scale_id, left_index, right_index)

        # Define list, which contains correct mms ids
        correct_mms_ids = get_correct_mms_ids(mms)

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

            is_s_exist = True

            # If that list contains even count
            # (more than 0) of zcs, then delete one of them
            if len(xtd_zcs_ids) % 2 == 0:
                xtd_zcs_ids.pop()

            s_zc_id = xtd_zcs_ids[0]
            s_zc_amplitude = zcs[s_zc_id].g_ampl
            for zc_id in range(xtd_zcs_ids[0], xtd_zcs_ids[0] + len(xtd_zcs_ids), 2):
                if zcs[zc_id].g_ampl > s_zc_amplitude:
                    s_zc_id = zc_id
                    s_zc_amplitude = zcs[s_zc_id].g_ampl

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
                    if float(dist_2) < float(QRSParams['GAMMA_SCALES_DIFF']) * float(dist_1):
                        xtd_zcs_ids.append(last_xtd_zc_id + 1)
                    else:
                        xtd_zcs_ids.pop()
                else:
                    xtd_zcs_ids.pop()

            # If S exist, it corresponds to odd zc with some big amplitude
            # If there is zcs after S-zc we should check them
            if is_s_exist:

                max_zc_id = xtd_zcs_ids[0]
                max_zc_amplitude = zcs[max_zc_id].g_ampl
                for zc_id in range(xtd_zcs_ids[0], xtd_zcs_ids[0] + len(xtd_zcs_ids), 2):
                    if zcs[zc_id].g_ampl > max_zc_amplitude:
                        max_zc_id = zc_id
                        max_zc_amplitude = zcs[s_zc_id].g_ampl

                s_zc_id = xtd_zcs_ids[0]
                s_zc_amplitude = zcs[s_zc_id].g_ampl
                for zc_id in range(xtd_zcs_ids[0], xtd_zcs_ids[0] + len(xtd_zcs_ids), 2):
                    if zcs[zc_id].g_ampl > max_zc_amplitude * float(QRSParams['GAMMA_RIGHT_S_PART']):
                        s_zc_id = zc_id
                        s_zc_amplitude = zcs[s_zc_id].g_ampl

                # Check zcs after S-zc
                if xtd_zcs_ids[-1] > s_zc_id:
                    after_s_zcs_ids = xtd_zcs_ids[xtd_zcs_ids.index(s_zc_id) + 1:]
                    if len(after_s_zcs_ids) % 2 == 1:
                        after_s_zcs_ids.pop()

                    # We check:
                    # * Difference between S-zc and next zc must be in allowed window - odd shift
                    # * Difference between zcs in M-morphology after S must be small - even shift
                    # * Amplitude of mm in M-morphology must be larger than some threshold
                    # If one of the conditions is passed then we should exclude xtd zcs
                    is_zcs_valid = True
                    odd_shift = int(float(QRSParams['GAMMA_RIGHT_ODD_XTD_ZCS_SHIFT']) * rate)
                    even_shift = int(float(QRSParams['GAMMA_RIGHT_EVEN_XTD_ZCS_SHIFT']) * rate)
                    mm_ampl = zcs[peak_zc_id].g_ampl * float(QRSParams['GAMMA_RIGHT_XTD_ZCS_MM_PART'])

                    for zc_id in after_s_zcs_ids[0:-1:2]:

                        if abs(zcs[zc_id].index - zcs[zc_id - 1].index) > odd_shift:
                            is_zcs_valid = False
                        if abs(zcs[zc_id + 1].index - zcs[zc_id].index) > even_shift:
                            is_zcs_valid = False
                        if abs(zcs[zc_id + 1].g_r_mm.value) < mm_ampl:
                            is_zcs_valid = False

                    if is_zcs_valid:
                        if len(after_s_zcs_ids) > 0:
                            xtd_zcs_ids = xtd_zcs_ids[0:xtd_zcs_ids.index(s_zc_id) + 1] + after_s_zcs_ids
                    else:
                        xtd_zcs_ids = xtd_zcs_ids[0:xtd_zcs_ids.index(s_zc_id) + 1]

    # Adding xtd points (including S)
    for xtd_point_zc_id in xtd_zcs_ids:

        if xtd_point_zc_id == s_zc_id and is_s_exist:
            s_zc_sign = morph_data.s_signs[scale_id]
            s_index = zcs[s_zc_id].index
            s_value = ecg_lead.filter[s_index]
            if s_zc_sign is ExtremumSign.positive:
                s_sign = WaveSign.positive
            else:
                s_sign = WaveSign.negative
            s_point = Point(PointName.s, s_index, s_value, s_sign)
            points.append(s_point)
        else:
            p_index = zcs[xtd_point_zc_id].index
            p_value = ecg_lead.filter[p_index]
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
