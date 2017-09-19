from Source.Model.main.delineation.p.peak import get_p_flexure_zc_id
from Source.Model.main.delineation.t.alpha.peak import get_t_flexure_zc_id
from Source.Model.main.delineation.wave_delineation import WaveSpecification
from Source.Model.main.params.p import PParams
from Source.Model.main.params.t import TParams


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
        delineation.special_points_indexes.append(zcs[left_peak_zc_id].index)
        delineation.special_points_indexes.append(zcs[right_peak_zc_id].index)