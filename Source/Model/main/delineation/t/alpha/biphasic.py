from Source.Model.main.delineation.p.peak import get_p_flexure_zc_id
from Source.Model.main.delineation.t.alpha.peak import get_t_flexure_zc_id
from Source.Model.main.delineation.wave_delineation import WaveSpecification
from Source.Model.main.params.p import PParams
from Source.Model.main.params.t import TParams
from Source.Model.main.delineation.t.zcs import *


def check_left_biphasic_t(triplet, ecg_lead, qrs_id, zcs, delineation):
    left_peak_zc_id = triplet.left_zc_id
    left_peak_zc = zcs[left_peak_zc_id]

    right_peak_zc_id = triplet.right_zc_id
    right_peak_zc = zcs[right_peak_zc_id]

    cur_qrs_dels_seq = ecg_lead.cur_qrs_dels_seq
    rr = cur_qrs_dels_seq[qrs_id].peak_index - cur_qrs_dels_seq[qrs_id - 1].peak_index

    if is_prev_zc_exist(zcs, left_peak_zc_id, rr):

        prev_zc_id = left_peak_zc_id - 1
        prev_zc = zcs[prev_zc_id]

        amplitude = abs(left_peak_zc.left_mm.value) + abs(right_peak_zc.right_mm.value)

        if prev_zc.mm_amplitude > amplitude * float(TParams['BIPHASIC_AMPLITUDE_LEFT']) \
                and distance_between_zcs(zcs, prev_zc_id, left_peak_zc_id) < rr * float(TParams['BIPHASIC_LIMIT_SHIFT']):
            delineation.specification = WaveSpecification.biphasic
            delineation.special_points_indexes.append(prev_zc.index)

            triplet.left_zc_id = prev_zc_id


def check_right_biphasic_t(triplet, ecg_lead, qrs_id, zcs, delineation):
    left_peak_zc_id = triplet.left_zc_id
    left_peak_zc = zcs[left_peak_zc_id]

    right_peak_zc_id = triplet.right_zc_id
    right_peak_zc = zcs[right_peak_zc_id]

    cur_qrs_dels_seq = ecg_lead.cur_qrs_dels_seq
    rr = cur_qrs_dels_seq[qrs_id].peak_index - cur_qrs_dels_seq[qrs_id - 1].peak_index

    if is_next_zc_exist(zcs, right_peak_zc_id, rr):

        next_zc_id = right_peak_zc_id + 1
        next_zc = zcs[next_zc_id]

        amplitude = abs(left_peak_zc.left_mm.value) + abs(right_peak_zc.right_mm.value)

        if next_zc.mm_amplitude > amplitude * float(TParams['BIPHASIC_AMPLITUDE_RIGHT']) \
                and distance_between_zcs(zcs, right_peak_zc_id, next_zc_id) < rr * float(TParams['BIPHASIC_LIMIT_SHIFT']):
            delineation.specification = WaveSpecification.biphasic
            delineation.special_points_indexes.append(next_zc.index)

            triplet.right_zc_id = next_zc_id