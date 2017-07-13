from Source.Model.main.delineation.morfology_point import *
from Source.Model.main.modulus_maxima.routines import *


def onset_processing(first_zc_id, ecg_lead, delineation, qrs_morphology_data, points, direction):

    # Init necessary data
    scale_id = qrs_morphology_data.scale_id
    wdc = qrs_morphology_data.wdc[scale_id]
    zcs = qrs_morphology_data.zcs[scale_id]
    begin_index = qrs_morphology_data.begin_index
    onset_index_beta = delineation.onset_index

    # Init onset index
    qrs_onset_index = onset_index_beta

    if first_zc_id >= 0:

        first_zc_index = zcs[first_zc_id].index

        # Onset searching
        is_onset_found = False

        # 1.  First check:
        #     If exist zc before onset (move from right to left),
        #     defined at the step beta,
        #     index of that zc defined as new onset.
        #     If count of that zcs is more than 1, choose last
        if not is_onset_found:

            onset_zcs_ids = []
            for zc_id in range(0, len(zcs)):
                if onset_index_beta <= zcs[zc_id].index < first_zc_index:
                    onset_zcs_ids.append(zc_id)

            if len(onset_zcs_ids) > 0:
                onset_zc_id = onset_zcs_ids[-1]
                qrs_onset_index = zcs[onset_zc_id].index
                is_onset_found = True

        # 2.  Second check:
        #     Form mms list and search last incorrect mm,
        #     which index defines as new onset
        if not is_onset_found:

            mms = []
            mm_curr = find_left_mm(first_zc_index, wdc)
            mm_next = mm_curr
            while mm_next.index > begin_index:
                mm_curr = mm_next
                mms.append(mm_curr)
                mm_next = find_left_mm(mm_curr.index - 1, wdc)

            mms_ids_incorrect = []
            for mm_id in range(0, len(mms)):
                if not mms[mm_id].correctness:
                    mms_ids_incorrect.append(mm_id)

            if len(mms) > 0:
                if len(mms_ids_incorrect) > 0:
                    mm_id_incorrect = mms_ids_incorrect[0]
                    qrs_onset_index = mms[mm_id_incorrect].index
                    is_onset_found = True

        # 3.  Last scenario:
        #     Init onset with onset from beta step
        if not is_onset_found:
            qrs_onset_index = onset_index_beta

        # Incrementation for separation
        qrs_onset_index -= 1

    # Including onset to morphology
    qrs_onset_value = ecg_lead.filtrated[qrs_onset_index]
    qrs_onset_sign = WaveSign.none
    qrs_onset_point = Point(PointName.qrs_onset, qrs_onset_index, qrs_onset_value, qrs_onset_sign)
    if direction < 0:
        points.insert(0, qrs_onset_point)
    else:
        points.append(qrs_onset_point)
    delineation.onset_index = qrs_onset_index

