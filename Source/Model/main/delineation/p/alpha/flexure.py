from Source.Model.main.params.p import PParams
from Source.Model.main.delineation.wave_delineation import WaveSpecification


def check_flexure_p(triplet, ecg_lead, qrs_id, zcs, delineation):

    zc_flexure_id = get_p_flexure_zc_id(ecg_lead, qrs_id, zcs, triplet.center_zc_id)

    if zc_flexure_id is not -1:
        peak_zc_id = zc_flexure_id
        left_peak_zc_id = zc_flexure_id - 1
        right_peak_zc_id = zc_flexure_id + 1

        triplet.left_zc_id = left_peak_zc_id
        triplet.center_zc_id = peak_zc_id
        triplet.right_zc_id = right_peak_zc_id

        delineation.specification = WaveSpecification.flexure
        delineation.peak_index = zcs[peak_zc_id].index

def get_p_flexure_zc_id(ecg_lead, qrs_id, zcs, peak_zc_id):

    qrs_dels = ecg_lead.qrs_dels

    flexure_zc_id = -1

    rr = qrs_dels[qrs_id].peak_index - qrs_dels[qrs_id - 1].peak_index

    for zc_id in range(1, len(zcs) - 1):
        if abs(zcs[zc_id - 1].index - zcs[zc_id].index) < float(PParams['ALPHA_FLEX_SHIFT']) * rr \
                and abs(zcs[zc_id + 1].index - zcs[zc_id].index) < float(PParams['ALPHA_FLEX_SHIFT']) * rr \
                and zcs[zc_id].mm_amplitude < float(PParams['ALPHA_FLEX_AMPL_NGBR']) * zcs[zc_id - 1].mm_amplitude \
                and zcs[zc_id].mm_amplitude < float(PParams['ALPHA_FLEX_AMPL_NGBR']) * zcs[zc_id + 1].mm_amplitude\
                and zcs[zc_id - 1].mm_amplitude > float(PParams['ALPHA_FLEX_AMPL_OLD_ZC']) * zcs[peak_zc_id].mm_amplitude\
                and zcs[zc_id + 1].mm_amplitude > float(PParams['ALPHA_FLEX_AMPL_OLD_ZC']) * zcs[peak_zc_id].mm_amplitude:
            flexure_zc_id = zc_id

    return flexure_zc_id