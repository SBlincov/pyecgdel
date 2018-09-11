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


def shift_all(leads, del_data, all_leads_data, corr_mtx, stat_data):

    num_leads = len(leads)

    for g_id in range(0, len(all_leads_data.borders_counts)):

        qrs_count = stat_data.counts[g_id]
        qrs_ons = stat_data.ons[g_id]
        qrs_peaks = stat_data.peaks[g_id]
        qrs_offs = stat_data.offs[g_id]

        if qrs_count > 0:

            mean_qrs_on = int(np.mean(qrs_ons))
            mean_qrs_peak = int(np.mean(qrs_peaks))
            mean_qrs_off = int(np.mean(qrs_offs))

            std_qrs_on = np.std(qrs_ons)
            std_qrs_peak = np.std(qrs_peaks)
            std_qrs_off = np.std(qrs_offs)

            # Check for shifting
            for lead_id in range(0, num_leads):

                mtx_id = corr_mtx[lead_id][g_id]

                if mtx_id > -1:

                    # Check shift branches
                    is_peak_shifted = is_qrs_peak_shifted(del_data, lead_id, mtx_id, mean_qrs_peak, std_qrs_peak)
                    branch_onset = get_qrs_on_shift_branch(del_data, lead_id, mtx_id, mean_qrs_on, std_qrs_on)
                    branch_offset = get_qrs_off_shift_branch(del_data, lead_id, mtx_id, mean_qrs_off, std_qrs_off)
                    num_points = len(leads[lead_id].qrs_morphs[mtx_id].points)

                    peak = del_data.peaks[lead_id][mtx_id]

                    if is_peak_shifted == False or num_points <= 5:

                        mms = leads[lead_id].mms[0]
                        indexes = [x.index for x in mms]

                        if (branch_onset > 0):

                            on = del_data.ons[lead_id][mtx_id]
                            new_on = on
                            new_on_left = on
                            new_on_right = on

                            mm_id_init = get_closest(indexes, mean_qrs_on)

                            # Search closest to mean left non-correct mms and zcs on 0 scale
                            mm_id = mm_id_init
                            if mms[mm_id].index > mean_qrs_on:
                                mm_id -= 1
                            mm_left = mms[mm_id]
                            left_zc_index = find_left_thc_index(leads[lead_id].wdc[0], mean_qrs_on, on, 0.0)

                            if mm_left.correctness is False:
                                new_on_left = max(mm_left.index, left_zc_index)
                            else:
                                new_on_left = left_zc_index

                            # Search closest to mean right non-correct mms and zcs on 0 scale
                            mm_id = mm_id_init
                            if mms[mm_id].index < mean_qrs_on:
                                mm_id += 1
                            mm_right = mms[mm_id]
                            right_zc_index = find_right_thc_index(leads[lead_id].wdc[0], mean_qrs_on, peak, 0.0)

                            if mm_right.correctness is False:
                                new_on_right = min(mm_right.index, right_zc_index)
                            else:
                                new_on_right = right_zc_index

                            # Now best from left and right
                            if abs(new_on_left - mean_qrs_on) > abs(new_on_right - mean_qrs_on):
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

                            mm_id_init = get_closest(indexes, mean_qrs_off)

                            # Search closest to mean left non-correct mms and zcs on 0 scale
                            mm_id = mm_id_init
                            if mms[mm_id].index > mean_qrs_off:
                                mm_id -= 1
                            mm_left = mms[mm_id]
                            left_zc_index = find_left_thc_index(leads[lead_id].wdc[0], mean_qrs_off, peak, 0.0)

                            if mm_left.correctness is False:
                                new_off_left = max(mm_left.index, left_zc_index)
                            else:
                                new_off_left = left_zc_index

                            # Search closest to mean left non-correct mms and zcs on 0 scale
                            mm_id = mm_id_init
                            if mms[mm_id].index < mean_qrs_off:
                                mm_id += 1
                            mm_right = mms[mm_id]
                            right_zc_index = find_right_thc_index(leads[lead_id].wdc[0], mean_qrs_off, off, 0.0)

                            if mm_right.correctness is False:
                                new_off_right = min(mm_right.index, right_zc_index)
                            else:
                                new_off_right = right_zc_index

                            # Now best from left and right
                            if abs(new_off_left - mean_qrs_off) > abs(new_off_right - mean_qrs_off):
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
                        qrs_del_extra_zcs = get_zcs_in_window(leads[lead_id].zcs[int(QRSParams['WDC_SCALE_ID'])], mean_qrs_on, mean_qrs_off)

                        # If ZCSs exist in averaged interval
                        if qrs_del_extra_zcs:

                            # Search ZCS with maximum mm_amplitude
                            qrs_del_extra_zc = qrs_del_extra_zcs[0]
                            for zc_id in range(1, len(qrs_del_extra_zcs)):
                                if qrs_del_extra_zcs[zc_id].g_ampl > qrs_del_extra_zc.g_ampl:
                                    qrs_del_extra_zc = qrs_del_extra_zcs[zc_id]

                            leads[lead_id].qrs_dels[mtx_id].onset_index = mean_qrs_on
                            leads[lead_id].qrs_dels[mtx_id].peak_index = qrs_del_extra_zc.index
                            leads[lead_id].qrs_dels[mtx_id].offset_index = mean_qrs_off

                            # Init morphology for new QRS
                            morphology = get_qrs_morphology(leads[lead_id], mtx_id, leads[lead_id].qrs_dels[mtx_id])
                            # We should not change del_id in morphology of new QRS

                            leads[lead_id].qrs_morphs[mtx_id] = morphology