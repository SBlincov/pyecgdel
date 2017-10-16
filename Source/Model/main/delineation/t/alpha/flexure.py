from Source.Model.main.delineation.wave_delineation import WaveSpecification
from Source.Model.main.params.t import TParams
from Source.Model.main.delineation.t.routines import get_t_begin_index, get_t_end_index


def check_flexure_t(triplet, ecg_lead, qrs_id, zcs, delineation):

    zc_flexure_id = get_t_flexure_zc_id(ecg_lead, qrs_id, zcs, triplet.center_zc_id)

    if zc_flexure_id is not -1:
        peak_zc_id = zc_flexure_id
        left_peak_zc_id = zc_flexure_id - 1
        right_peak_zc_id = zc_flexure_id + 1

        triplet.left_zc_id = left_peak_zc_id
        triplet.center_zc_id = peak_zc_id
        triplet.right_zc_id = right_peak_zc_id

        delineation.specification = WaveSpecification.flexure
        delineation.peak_index = zcs[peak_zc_id].index
        # delineation.special_points_indexes.append(zcs[left_peak_zc_id].index)
        # delineation.special_points_indexes.append(zcs[right_peak_zc_id].index)


def get_t_flexure_zc_id(ecg_lead, qrs_id, zcs, peak_zc_id):

    qrs_dels = ecg_lead.qrs_dels

    flexure_zc_id = -1

    rr = qrs_dels[qrs_id].peak_index - qrs_dels[qrs_id - 1].peak_index

    begin_index = get_t_begin_index(ecg_lead, qrs_id)
    end_index = get_t_end_index(ecg_lead, qrs_id)

    zcs_peaks_begin_index = begin_index
    zcs_peaks_end_index = end_index
    zcs_peaks_window = zcs_peaks_end_index - zcs_peaks_begin_index

    for zc_id in range(1, len(zcs) - 1):
        flex_begin = zcs_peaks_begin_index + int(zcs_peaks_window * float(TParams['ALPHA_FLEX_BEGIN_PART']))
        flex_end = zcs_peaks_begin_index + int(zcs_peaks_window * float(TParams['ALPHA_FLEX_END_PART']))
        if flex_begin < zcs[zc_id].index < flex_end:
            if abs(zcs[zc_id - 1].index - zcs[zc_id].index) < float(TParams['ALPHA_FLEX_SHIFT']) * rr \
                    and abs(zcs[zc_id + 1].index - zcs[zc_id].index) < float(TParams['ALPHA_FLEX_SHIFT']) * rr \
                    and zcs[zc_id].mm_amplitude < float(TParams['ALPHA_FLEX_AMPL_NGBR']) * zcs[zc_id - 1].mm_amplitude \
                    and zcs[zc_id].mm_amplitude < float(TParams['ALPHA_FLEX_AMPL_NGBR']) * zcs[zc_id + 1].mm_amplitude\
                    and zcs[zc_id - 1].mm_amplitude > float(TParams['ALPHA_FLEX_AMPL_OLD_ZC']) * zcs[peak_zc_id].mm_amplitude\
                    and zcs[zc_id + 1].mm_amplitude > float(TParams['ALPHA_FLEX_AMPL_OLD_ZC']) * zcs[peak_zc_id].mm_amplitude:
                flexure_zc_id = zc_id

    return flexure_zc_id
