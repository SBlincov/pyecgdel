from Source.Model.main.delineation.peaks_zcs_ids import PeakZCsIds
from Source.Model.main.delineation.p.beta.peak import get_p_peak_zc_id, is_p_peak_zc_candidate_exist, is_small_p
from Source.Model.main.delineation.p.beta.flexure import check_flexure_p
from Source.Model.main.delineation.p.beta.biphasic import check_left_biphasic_p, check_right_biphasic_p
from Source.Model.main.delineation.p.beta.onset import define_p_onset_index
from Source.Model.main.delineation.p.beta.offset import define_p_offset_index
from Source.Model.main.delineation.p.beta.legacy import check_for_atrial_fibrillation
from Source.Model.main.delineation.p.routines import get_p_begin_index, get_p_end_index
from Source.Model.main.delineation.p.zcs import get_p_zcs
from Source.Model.main.delineation.wave_delineation import WaveDelineation, WaveSpecification
from Source.Model.main.delineation.p.routines import get_window

from Source.Model.main.params.p import PParams


def get_p_del(ecg_lead, qrs_id):

    delineation = WaveDelineation()

    if ecg_lead.qrs_dels[qrs_id].specification is WaveSpecification.extra:
        return delineation

    rate = ecg_lead.rate

    mm_window = int(float(PParams['ALPHA_MM_WINDOW']) * rate)

    zcs = get_p_zcs(ecg_lead, qrs_id, mm_window)

    if not zcs:
        return delineation

    if ((zcs[-1].s_r_mm.index - zcs[-1].index) > int(float(PParams['ALPHA_RIGHT_MM_DIST']) * rate)) or (abs(zcs[-1].s_r_mm.value) / abs(zcs[-1].s_l_mm.value) > float(PParams['ALPHA_OFFSET_MM_SHARP'])):
        zcs.pop(-1)

    if not zcs:
        return delineation

    if ((zcs[0].index - zcs[0].s_l_mm.index) > int(float(PParams['ALPHA_LEFT_MM_DIST']) * rate)) or (abs(zcs[0].s_l_mm.value) / abs(zcs[0].s_r_mm.value) > float(PParams['ALPHA_ONSET_MM_SHARP'])):
        zcs.pop(0)

    if not zcs:
        return delineation

    window = get_window(ecg_lead, qrs_id)
    begin_index = get_p_begin_index(ecg_lead, qrs_id)
    end_index = get_p_end_index(ecg_lead, qrs_id)

    if window < int(float(PParams['ALPHA_PEAK_BEGIN_SHIFT']) * rate):
        return delineation

    if not is_p_peak_zc_candidate_exist(ecg_lead, qrs_id, zcs):
        return delineation

    peak_zc_id = get_p_peak_zc_id(ecg_lead, qrs_id, zcs)

    if is_small_p(ecg_lead, qrs_id, zcs, peak_zc_id):
        return delineation

    peak_zc = zcs[peak_zc_id]
    peak_index = peak_zc.index
    delineation.peak_index = peak_index
    delineation.specification = WaveSpecification.exist

    peak_zcs_ids = PeakZCsIds(peak_zc_id, peak_zc_id, peak_zc_id)

    check_flexure_p(peak_zcs_ids, ecg_lead, qrs_id, zcs, delineation)

    check_left_biphasic_p(peak_zcs_ids, ecg_lead, zcs, delineation)

    define_p_onset_index(ecg_lead, delineation, zcs, peak_zcs_ids.left_zc_id, begin_index)
    define_p_offset_index(ecg_lead, delineation, zcs, peak_zcs_ids.right_zc_id, end_index)

    check_for_atrial_fibrillation(delineation, zcs)

    return delineation