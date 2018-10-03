from Source.Model.main.delineation.qrs.delta.data import *
from Source.Model.main.zero_crossings.routines import *
from Source.Model.main.threshold_crossings.routines import *
from Source.Model.main.delineation.morfology_point import *
from Source.Model.main.delineation.qrs.gamma.gamma import *
from Source.Model.main.search.closest_position import *

def get_qrs_on_shift_branch(del_data, lead_id, mtx_id, mean_qrs_on, std_qrs_on):

    on = del_data.ons[lead_id][mtx_id]

    if on < mean_qrs_on:

        large_shift_lim = mean_qrs_on - QRSParams['DELTA_ON_LARGE_SHIFT_LEFT'] * std_qrs_on
        small_shift_lim = mean_qrs_on - QRSParams['DELTA_ON_SMALL_SHIFT_LEFT'] * std_qrs_on

        if on > small_shift_lim:
            return 0
        elif large_shift_lim < on <= small_shift_lim:
            return 1
        else:
            return 2

    else:

        large_shift_lim = mean_qrs_on + QRSParams['DELTA_ON_LARGE_SHIFT_RIGHT'] * std_qrs_on
        small_shift_lim = mean_qrs_on + QRSParams['DELTA_ON_SMALL_SHIFT_RIGHT'] * std_qrs_on

        if on < small_shift_lim:
            return 0
        elif small_shift_lim <= on < large_shift_lim:
            return 1
        else:
            return 2

def get_qrs_off_shift_branch(del_data, lead_id, mtx_id, mean_qrs_off, std_qrs_off):

    off = del_data.offs[lead_id][mtx_id]

    if off < mean_qrs_off:

        large_shift_lim = mean_qrs_off - QRSParams['DELTA_OFF_LARGE_SHIFT_LEFT'] * std_qrs_off
        small_shift_lim = mean_qrs_off - QRSParams['DELTA_OFF_SMALL_SHIFT_LEFT'] * std_qrs_off

        if off > small_shift_lim:
            return 0
        elif large_shift_lim < off <= small_shift_lim:
            return 1
        else:
            return 2

    else:

        large_shift_lim = mean_qrs_off + QRSParams['DELTA_OFF_LARGE_SHIFT_RIGHT'] * std_qrs_off
        small_shift_lim = mean_qrs_off + QRSParams['DELTA_OFF_SMALL_SHIFT_RIGHT'] * std_qrs_off

        if off < small_shift_lim:
            return 0
        elif small_shift_lim <= off < large_shift_lim:
            return 1
        else:
            return 2


def is_qrs_peak_shifted(del_data, lead_id, mtx_id, mean_qrs_peak, std_qrs_peak):

    peak = del_data.peaks[lead_id][mtx_id]
    right_lim = mean_qrs_peak + QRSParams['DELTA_PEAK_SHIFT'] * std_qrs_peak
    left_lim = mean_qrs_peak - QRSParams['DELTA_PEAK_SHIFT'] * std_qrs_peak

    if left_lim <= peak <= right_lim:
        return False
    else:
        return True


def shift_all(leads, del_data, integral_data):

    mtx = integral_data.mtx

    for del_id in range(0, integral_data.num_dels):

        count = integral_data.counts[del_id]
        ons = integral_data.ons[del_id]
        peaks = integral_data.peaks[del_id]
        offs = integral_data.offs[del_id]

        if count > 0:

            mean_ons = int(np.mean(ons))
            mean_peaks = int(np.mean(peaks))
            mean_offs = int(np.mean(offs))

            std_ons = np.std(ons)
            std_peaks = np.std(peaks)
            std_offs = np.std(offs)

            # Check for shifting
            for lead_id in range(0, del_data.num_leads):

                mtx_id = mtx[lead_id][del_id]

                if mtx_id > -1:

                    # Check shift branches
                    is_peak_shifted = is_qrs_peak_shifted(del_data, lead_id, mtx_id, mean_peaks, std_peaks)
                    branch_onset = get_qrs_on_shift_branch(del_data, lead_id, mtx_id, mean_ons, std_ons)
                    branch_offset = get_qrs_off_shift_branch(del_data, lead_id, mtx_id, mean_offs, std_offs)
                    num_points = len(leads[lead_id].qrs_morphs[mtx_id].points)

                    peak = del_data.peaks[lead_id][mtx_id]

                    if is_peak_shifted == False or num_points <= 5:

                        mms = leads[lead_id].mms[0]
                        ids_mms = leads[lead_id].ids_mms[0]

                        if (branch_onset > 0):

                            on = del_data.ons[lead_id][mtx_id]
                            new_on = on
                            new_on_left = on
                            new_on_right = on

                            mm_id_init = get_closest_mm_id(mms, ids_mms, mean_ons)

                            # Search closest to mean left non-correct mms and zcs on 0 scale
                            mm_id = mm_id_init
                            if mms[mm_id].index > mean_ons:
                                mm_id -= 1
                            mm_left = mms[mm_id]
                            left_zc_index = find_left_thc_index(leads[lead_id].wdc[0], mean_ons, on, 0.0)

                            if mm_left.correctness is False:
                                new_on_left = max(mm_left.index, left_zc_index)
                            else:
                                new_on_left = left_zc_index

                            # Search closest to mean right non-correct mms and zcs on 0 scale
                            mm_id = mm_id_init
                            if mms[mm_id].index < mean_ons:
                                mm_id += 1
                            mm_right = mms[mm_id]
                            right_zc_index = find_right_thc_index(leads[lead_id].wdc[0], mean_ons, peak, 0.0)

                            if mm_right.correctness is False:
                                new_on_right = min(mm_right.index, right_zc_index)
                            else:
                                new_on_right = right_zc_index

                            # Now best from left and right
                            if abs(new_on_left - mean_ons) > abs(new_on_right - mean_ons):
                                new_on = new_on_right
                            else:
                                new_on = new_on_left

                            # Refresh with new values
                            points = leads[lead_id].qrs_morphs[mtx_id].points
                            del points[0] # Delete current onset
                            start_p_id = 0
                            for p_id in range(0, len(points)):
                                if points[p_id].name == PointName.r or points[p_id].index > new_on:
                                    break
                                else:
                                    start_p_id += 1

                            points[0:start_p_id] = [] # Delete all unnecessary

                            new_on_point = Point(PointName.qrs_onset, new_on, leads[lead_id].filter[new_on], WaveSign.none)
                            points.insert(0, new_on_point)

                            leads[lead_id].qrs_dels[mtx_id].onset_index = new_on

                        if (branch_offset > 0):

                            off = del_data.offs[lead_id][mtx_id]
                            new_off = off
                            new_off_left = off
                            new_off_right = off

                            mm_id_init = get_closest_mm_id(mms, ids_mms, mean_offs)

                            # Search closest to mean left non-correct mms and zcs on 0 scale
                            mm_id = mm_id_init
                            if mms[mm_id].index > mean_offs:
                                mm_id -= 1
                            mm_left = mms[mm_id]
                            left_zc_index = find_left_thc_index(leads[lead_id].wdc[0], mean_offs, peak, 0.0)

                            if mm_left.correctness is False:
                                new_off_left = max(mm_left.index, left_zc_index)
                            else:
                                new_off_left = left_zc_index

                            # Search closest to mean left non-correct mms and zcs on 0 scale
                            mm_id = mm_id_init
                            if mms[mm_id].index < mean_offs:
                                mm_id += 1
                            mm_right = mms[mm_id]
                            right_zc_index = find_right_thc_index(leads[lead_id].wdc[0], mean_offs, off, 0.0)

                            if mm_right.correctness is False:
                                new_off_right = min(mm_right.index, right_zc_index)
                            else:
                                new_off_right = right_zc_index

                            # Now best from left and right
                            if abs(new_off_left - mean_offs) > abs(new_off_right - mean_offs):
                                new_off = new_off_right
                            else:
                                new_off = new_off_left

                            # Refresh with new values
                            points = leads[lead_id].qrs_morphs[mtx_id].points
                            points.pop()  # Delete current onset
                            start_p_id = len(points)
                            for p_id in range(len(points) - 1, -1, -1):
                                if points[p_id].name == PointName.r or points[p_id].index < new_off:
                                    break
                                else:
                                    start_p_id -= 1

                            points[start_p_id:] = []  # Delete all unnecessary

                            new_on_point = Point(PointName.qrs_offset, new_off, leads[lead_id].filter[new_off],
                                                 WaveSign.none)
                            points.append(new_on_point)

                            leads[lead_id].qrs_dels[mtx_id].offset_index = new_off

                    else:

                        # New delineation and morphology
                        qrs_del_extra_zcs = get_zcs_in_window(leads[lead_id].wdc[int(QRSParams['WDC_SCALE_ID'])],
                                                              leads[lead_id].zcs[int(QRSParams['WDC_SCALE_ID'])],
                                                              leads[lead_id].ids_zcs[int(QRSParams['WDC_SCALE_ID'])],
                                                              mean_ons,
                                                              mean_offs)

                        # If ZCSs exist in averaged interval
                        if qrs_del_extra_zcs:

                            # Search ZCS with maximum mm_amplitude
                            qrs_del_extra_zc = qrs_del_extra_zcs[0]
                            for zc_id in range(1, len(qrs_del_extra_zcs)):
                                if qrs_del_extra_zcs[zc_id].g_ampl > qrs_del_extra_zc.g_ampl:
                                    qrs_del_extra_zc = qrs_del_extra_zcs[zc_id]

                            leads[lead_id].qrs_dels[mtx_id].onset_index = mean_ons
                            leads[lead_id].qrs_dels[mtx_id].peak_index = qrs_del_extra_zc.index
                            leads[lead_id].qrs_dels[mtx_id].offset_index = mean_offs

                            # Init morphology for new QRS
                            morphology = get_qrs_morphology(leads[lead_id], mtx_id, leads[lead_id].qrs_dels[mtx_id])
                            # We should not change del_id in morphology of new QRS

                            leads[lead_id].qrs_morphs[mtx_id] = morphology