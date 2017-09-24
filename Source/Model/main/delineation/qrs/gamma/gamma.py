from Source.Model.main.delineation.qrs.gamma.data import *
from Source.Model.main.delineation.qrs.gamma.left import *
from Source.Model.main.delineation.qrs.gamma.right import *
from Source.Model.main.delineation.qrs.gamma.branches import *


def get_qrs_morphology(ecg_lead, del_id, delineation):

    scale_id = 0

    qrs_morphology_data = QRSMorphologyData(ecg_lead, delineation, scale_id)
    r_zc_id = qrs_morphology_data.peak_zcs_ids[scale_id]

    is_left_complex, first_zc_id, left_points = left_qrs_morphology(ecg_lead, delineation, qrs_morphology_data)
    is_right_complex, last_zc_id, right_points = right_qrs_morphology(ecg_lead, delineation, qrs_morphology_data)

    if is_left_complex:
        q_zc_id_diff = first_zc_id - r_zc_id
    else:
        q_zc_id_diff = -1

    if is_right_complex:
        s_zc_id_diff = last_zc_id - r_zc_id
    else:
        s_zc_id_diff = 1

    branch_id = []

    if is_left_complex is True and is_right_complex is True:
        branch_id.append(1)
        points = borders_processing(ecg_lead, delineation, qrs_morphology_data,
                                    q_zc_id_diff, left_points,
                                    s_zc_id_diff, right_points,
                                    branch_id)

    elif is_left_complex is True and is_right_complex is False:
        branch_id.append(2)
        points = borders_processing(ecg_lead, delineation, qrs_morphology_data,
                                    q_zc_id_diff, left_points,
                                    s_zc_id_diff, right_points,
                                    branch_id)

    elif is_left_complex is False and is_right_complex is True:
        branch_id.append(3)
        points = borders_processing(ecg_lead, delineation, qrs_morphology_data,
                                    q_zc_id_diff, left_points,
                                    s_zc_id_diff, right_points,
                                    branch_id)

    else:
        branch_id.append(0)
        points = borders_processing(ecg_lead, delineation, qrs_morphology_data,
                                    q_zc_id_diff, left_points,
                                    s_zc_id_diff, right_points,
                                    branch_id)

    degree = Degree.satisfyingly

    morphology = Morphology(del_id, points, degree, branch_id)

    return morphology

