from Source.Model.main.delineation.morfology_point import *
from Source.Model.main.modulus_maxima.routines import *
from Source.Model.main.params.qrs import *


def offset_processing(last_zc_id, ecg_lead, delineation, morph_data, points, direction):
    rate = ecg_lead.rate

    # Init necessary data
    scale_id = morph_data.scale_id
    peak_zc_id = morph_data.peak_zcs_ids[scale_id]
    wdc = morph_data.wdc[scale_id]
    zcs = morph_data.zcs[scale_id]
    end_index = morph_data.end_index
    offset_index_beta = delineation.offset_index
    all_mms = ecg_lead.mms[scale_id]

    # Init offset index
    qrs_offset_index = offset_index_beta

    if last_zc_id < len(zcs):

        last_zc = zcs[last_zc_id]

        # Begin of allowed interval
        right_lim = last_zc.index + int(float(QRSParams['GAMMA_RIGHT_WINDOW']) * rate)

        # Offset searching
        is_offset_found = False

        # Threshold for M-morphology
        mm_ampl = zcs[peak_zc_id].g_ampl * float(QRSParams['GAMMA_RIGHT_XTD_ZCS_MM_PART'])

        # 1.  First check:
        #     If exist zc before offset, defined at the step beta,
        #     index of that zc defined as new offset.
        #     If count of that zcs is more than 1, choose first
        if not is_offset_found:

            offset_zcs_ids = []
            for zc_id in range(0, len(zcs)):
                if last_zc.index < zcs[zc_id].index <= offset_index_beta:
                    offset_zcs_ids.append(zc_id)

            # We check 2 options:
            # * zc in small window
            # * zc left mm is big
            # If at least one is passed, offset defines here

            if len(offset_zcs_ids) > 0:
                offset_zc_id = offset_zcs_ids[0]
                if zcs[offset_zc_id].index <= right_lim:
                    qrs_offset_index = zcs[offset_zc_id].index
                    is_offset_found = True
                if abs(zcs[offset_zc_id].g_l_mm.value) > mm_ampl:
                    qrs_offset_index = zcs[offset_zc_id].index
                    is_offset_found = True

        # 2.  Second check:
        #     Form mms list and search incorrect mm,
        #     which index defines as new offset
        if not is_offset_found:

            mms = []
            mm_curr = last_zc.r_mms[0]
            mm_next = mm_curr
            while mm_next.index < end_index:
                mm_curr = mm_next
                mms.append(mm_curr)
                mm_next = all_mms[mm_curr.id + 1]

            mms_ids_incorrect = []
            for mm_id in range(0, len(mms)):
                if not mms[mm_id].correctness:
                    mms_ids_incorrect.append(mm_id)

            if len(mms) > 0:
                if len(mms_ids_incorrect) > 0:
                    if abs(zcs[last_zc_id].g_r_mm.value) > mm_ampl:
                        mm_id_incorrect = mms_ids_incorrect[-1]
                        qrs_offset_index = mms[mm_id_incorrect].index
                        is_offset_found = True
                    else:
                        for mm_id in mms_ids_incorrect:
                            if mms[mm_id].index <= right_lim:
                                qrs_offset_index = mms[mm_id].index
                                is_offset_found = True

        # 3.  Third check:
        #     In allowed window exist only correct mms,
        #     then we looking for correct mm on special scale in allowed interval
        #     and define its index as onset
        if not is_offset_found:
            scale_id_bord = int(QRSParams['GAMMA_BORD_SCALE'])
            target_index = last_zc.index
            indexes = [x.index for x in ecg_lead.zcs[scale_id_bord]]
            target_id = get_closest(indexes, target_index)
            tmp_zc = ecg_lead.zcs[scale_id_bord][target_id]
            mm_bord = tmp_zc.r_mms[0]
            qrs_offset_index = mm_bord.index
            is_offset_found = True

        # 4.  Last scenario:
        #     Init offset with offset from beta step
        if not is_offset_found:
            qrs_offset_index = offset_index_beta

    # Including offset to morphology
    qrs_offset_value = ecg_lead.filter[qrs_offset_index]
    qrs_offset_sign = WaveSign.none
    qrs_offset_point = Point(PointName.qrs_offset, qrs_offset_index, qrs_offset_value, qrs_offset_sign)
    if direction < 0:
        points.insert(0, qrs_offset_point)
    else:
        points.append(qrs_offset_point)
    delineation.offset_index = qrs_offset_index

