from Source.Model.main.delineation.morfology_point import *
from Source.Model.main.modulus_maxima.routines import *
from Source.Model.main.params.qrs import *


def onset_processing(first_zc_id, ecg_lead, delineation, qrs_morphology_data, points, direction):

    rate = ecg_lead.rate

    # Init necessary data
    scale_id = qrs_morphology_data.scale_id
    peak_zc_id = qrs_morphology_data.peak_zcs_ids[scale_id]
    wdc = qrs_morphology_data.wdc[scale_id]
    zcs = qrs_morphology_data.zcs[scale_id]
    begin_index = qrs_morphology_data.begin_index
    onset_index_beta = delineation.onset_index

    # Init onset index
    qrs_onset_index = onset_index_beta

    if first_zc_id >= 0:

        first_zc_index = zcs[first_zc_id].index

        # Begin of allowed interval
        left_lim = first_zc_index - int(float(QRSParams['GAMMA_LEFT_WINDOW']) * rate)

        # Onset searching
        is_onset_found = False

        # Threshold for M-morphology
        mm_ampl = zcs[peak_zc_id].mm_amplitude * float(QRSParams['GAMMA_LEFT_XTD_ZCS_MM_PART'])

        # 1.  First check:
        #     If exist zc before onset (move from right to left), defined at the step beta,
        #     index of that zc defined as new onset.
        #     If count of that zcs is more than 1, choose last
        if not is_onset_found:

            onset_zcs_ids = []
            for zc_id in range(0, len(zcs)):
                if onset_index_beta <= zcs[zc_id].index < first_zc_index:
                    onset_zcs_ids.append(zc_id)

            # We check 2 options:
            # * zc in small window
            # * zc right mm is big
            # If at least one is passed, onset defines here

            if len(onset_zcs_ids) > 0:
                onset_zc_id = onset_zcs_ids[-1]
                if zcs[onset_zc_id].index >= left_lim:
                    qrs_onset_index = zcs[onset_zc_id].index
                    is_onset_found = True
                if abs(zcs[onset_zc_id].right_mm.value) > mm_ampl:
                    qrs_onset_index = zcs[onset_zc_id].index
                    is_onset_found = True

        # 2.  Second check:
        #     Form mms list and search incorrect mm,
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
                    if abs(zcs[first_zc_id].left_mm.value) > mm_ampl:
                        mm_id_incorrect = mms_ids_incorrect[0]
                        qrs_onset_index = mms[mm_id_incorrect].index
                        is_onset_found = True
                    else:
                        for mm_id in mms_ids_incorrect:
                            if mms[mm_id].index >= left_lim:
                                qrs_onset_index = mms[mm_id].index
                                is_onset_found = True

        # 3.  Third check:
        #     In allowed window exist only correct mms,
        #     then we looking for correct mm on special scale in allowed interval
        #     and define its index as onset
        if not is_onset_found:
            scale_id_bord = int(QRSParams['GAMMA_BORD_SCALE'])
            wdc_bord = qrs_morphology_data.wdc[scale_id_bord]
            mm_bord = find_left_mm(first_zc_index, wdc_bord)
            qrs_onset_index = mm_bord.index
            is_onset_found = True

        # 4.  Last scenario:
        #     Init onset with onset from beta step
        if not is_onset_found:
            qrs_onset_index = onset_index_beta

    # Including onset to morphology
    qrs_onset_value = ecg_lead.filter[qrs_onset_index]
    qrs_onset_sign = WaveSign.none
    qrs_onset_point = Point(PointName.qrs_onset, qrs_onset_index, qrs_onset_value, qrs_onset_sign)
    if direction < 0:
        points.insert(0, qrs_onset_point)
    else:
        points.append(qrs_onset_point)
    delineation.onset_index = qrs_onset_index

