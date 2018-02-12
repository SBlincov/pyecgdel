from Source.Model.main.delineation.peaks_zcs_ids import PeakZCsIds
from Source.Model.main.delineation.t.alpha.biphasic import check_left_biphasic_t
from Source.Model.main.delineation.t.alpha.biphasic import check_right_biphasic_t
from Source.Model.main.delineation.t.alpha.flexure import check_flexure_t
from Source.Model.main.delineation.t.alpha.offset import define_t_offset_index
from Source.Model.main.delineation.t.alpha.onset import define_t_onset_index
from Source.Model.main.delineation.t.alpha.peak import get_t_peak_zc_id
from Source.Model.main.delineation.t.routines import get_t_begin_index, get_t_end_index
from Source.Model.main.delineation.t.zcs import get_t_zcs
from Source.Model.main.delineation.wave_delineation import WaveDelineation, WaveSpecification
from Source.Model.main.params.t import TParams


def get_t_delineation(ecg_lead, qrs_id):

    rate = ecg_lead.rate

    delineation = WaveDelineation()

    # First check for T existing:
    #     If gap between two neighbor QRS is less than shift from QRS for searching T,
    #     Then there is no T
    qrs_gap = ecg_lead.qrs_dels[qrs_id].onset_index - ecg_lead.qrs_dels[qrs_id - 1].offset_index
    shift = int(float(TParams['ALPHA_QRS_BTW']) * rate)
    if shift >= qrs_gap:
        delineation.specification = WaveSpecification.absence
        return delineation

    # Get zcs - candidates for T in allowed interval
    mm_window = int(float(TParams['ALPHA_MM_WINDOW']) * rate)
    zcs = get_t_zcs(ecg_lead, qrs_id, mm_window)

    # Second check for T existing:
    #     If there is no zcs candidates for T
    #     Then there is no T
    if not zcs:
        delineation.specification = WaveSpecification.absence
        return delineation

    # Third check:
    #     If first zc has very big left mm - it means that it corresponds to S
    #     (we assume that QRS is separated from T)
    #     Then pop it from first position and check for existing another zcs
    if abs(zcs[0].left_mm.value) / abs(zcs[0].right_mm.value) > float(TParams['ALPHA_MM_SHARP']):
        zcs.pop(0)
    if not zcs:
        return delineation

    # Getting borders indexes for T delineation
    begin_index = get_t_begin_index(ecg_lead, qrs_id)
    end_index = get_t_end_index(ecg_lead, qrs_id)

    # Get peak index
    peak_zc_id = get_t_peak_zc_id(ecg_lead, qrs_id, zcs)

    # Init delineation
    peak_zc = zcs[peak_zc_id]
    peak_index = peak_zc.index
    delineation.peak_index = peak_index
    delineation.specification = WaveSpecification.exist

    # Creating triplets
    peak_zcs_ids = PeakZCsIds(peak_zc_id, peak_zc_id, peak_zc_id)

    # Analyzing complex cases
    check_flexure_t(peak_zcs_ids, ecg_lead, qrs_id, zcs, delineation)
    check_left_biphasic_t(peak_zcs_ids, ecg_lead, qrs_id, zcs, delineation)
    check_right_biphasic_t(peak_zcs_ids, ecg_lead, qrs_id, zcs, delineation)

    # Defining onset and offset
    define_t_onset_index(ecg_lead, delineation, zcs, peak_zcs_ids.left_zc_id, begin_index)
    define_t_offset_index(ecg_lead, delineation, zcs, peak_zcs_ids.right_zc_id, end_index)

    return delineation
