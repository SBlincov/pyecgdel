from Source.Model.main.delineation.morfology_point import *
from Source.Model.main.modulus_maxima.routines import *


def offset_processing(last_zc_id, ecg_lead, delineation, qrs_morphology_data, points, direction):

    # Init necessary data
    scale_id = qrs_morphology_data.scale_id
    wdc = qrs_morphology_data.wdc[scale_id]
    zcs = qrs_morphology_data.zcs[scale_id]
    end_index = qrs_morphology_data.end_index
    offset_index_beta = delineation.offset_index

    # Init offset index
    qrs_offset_index = offset_index_beta

    if last_zc_id < len(zcs):

        last_zc_index = zcs[last_zc_id].index

        # Offset searching
        is_offset_found = False

        # 1.  First check:
        #     If exist zc before offset, defined at the step beta,
        #     index of that zc defined as new offset.
        #     If count of that zcs is more than 1, choose first
        if not is_offset_found:

            offset_zcs_ids = []
            for zc_id in range(0, len(zcs)):
                if last_zc_index < zcs[zc_id].index <= offset_index_beta:
                    offset_zcs_ids.append(zc_id)

            if len(offset_zcs_ids) > 0:
                offset_zc_id = offset_zcs_ids[0]
                qrs_offset_index = zcs[offset_zc_id].index
                is_offset_found = True

        # 2.  Second check:
        #     Form mms list and search last incorrect mm,
        #     which index defines as new offset
        if not is_offset_found:

            mms = []
            mm_curr = find_right_mm(last_zc_index, wdc)
            mm_next = mm_curr
            while mm_next.index < end_index:
                mm_curr = mm_next
                mms.append(mm_curr)
                mm_next = find_right_mm(mm_curr.index + 1, wdc)

            mms_ids_incorrect = []
            for mm_id in range(0, len(mms)):
                if not mms[mm_id].correctness:
                    mms_ids_incorrect.append(mm_id)

            if len(mms) > 0:
                if len(mms_ids_incorrect) > 0:
                    mm_id_incorrect = mms_ids_incorrect[-1]
                    qrs_offset_index = mms[mm_id_incorrect].index
                    is_offset_found = True

        # 3.  Last scenario:
        #     Init offset with offset from beta step
        if not is_offset_found:
            qrs_offset_index = offset_index_beta

        # Incrementation for separation
        qrs_offset_index += 1

    # Including offset to morphology
    qrs_offset_value = ecg_lead.filtrated[qrs_offset_index]
    qrs_offset_sign = WaveSign.none
    qrs_offset_point = Point(PointName.qrs_offset, qrs_offset_index, qrs_offset_value, qrs_offset_sign)
    if direction < 0:
        points.insert(0, qrs_offset_point)
    else:
        points.append(qrs_offset_point)
    delineation.offset_index = qrs_offset_index

