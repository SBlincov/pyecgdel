from Source.Model.main.delineation.qrs.gamma.data import *
from Source.Model.main.delineation.qrs.gamma.peak import *
from Source.Model.main.delineation.qrs.gamma.onset import *
from Source.Model.main.delineation.qrs.gamma.offset import *


def q_r_s_processing(ecg_lead, delineation, qrs_morphology_data, q_zc_id_diff, left_points, s_zc_id_diff, right_points):

    points = []

    scale_id = qrs_morphology_data.scale_id

    r_zc_id = qrs_morphology_data.peak_zcs_ids[scale_id]
    q_zc_id = r_zc_id + q_zc_id_diff
    s_zc_id = r_zc_id + s_zc_id_diff

    if left_points:
        points = left_points + points
    onset_processing(q_zc_id, ecg_lead, delineation, qrs_morphology_data, points, -1)
    qrs_morphology_data = QRSMorphologyData(ecg_lead, delineation, scale_id)

    r_zc_id = qrs_morphology_data.peak_zcs_ids[scale_id]
    q_zc_id = r_zc_id + q_zc_id_diff
    s_zc_id = r_zc_id + s_zc_id_diff

    r_processing(r_zc_id, ecg_lead, delineation, qrs_morphology_data, points, 1)
    qrs_morphology_data = QRSMorphologyData(ecg_lead, delineation, scale_id)

    r_zc_id = qrs_morphology_data.peak_zcs_ids[scale_id]
    q_zc_id = r_zc_id + q_zc_id_diff
    s_zc_id = r_zc_id + s_zc_id_diff

    if right_points:
        points = points + right_points
    offset_processing(s_zc_id, ecg_lead, delineation, qrs_morphology_data, points, 1)
    qrs_morphology_data = QRSMorphologyData(ecg_lead, delineation, scale_id)

    return points


def s_r_q_processing(ecg_lead, delineation, qrs_morphology_data, q_zc_id_diff, left_points, s_zc_id_diff, right_points):

    points = []

    scale_id = qrs_morphology_data.scale_id

    r_zc_id = qrs_morphology_data.peak_zcs_ids[scale_id]
    q_zc_id = r_zc_id + q_zc_id_diff
    s_zc_id = r_zc_id + s_zc_id_diff

    if right_points:
        points = points + right_points
    offset_processing(s_zc_id, ecg_lead, delineation, qrs_morphology_data, points, 1)
    qrs_morphology_data = QRSMorphologyData(ecg_lead, delineation, scale_id)

    r_zc_id = qrs_morphology_data.peak_zcs_ids[scale_id]
    q_zc_id = r_zc_id + q_zc_id_diff
    s_zc_id = r_zc_id + s_zc_id_diff

    r_processing(r_zc_id, ecg_lead, delineation, qrs_morphology_data, points, -1)
    qrs_morphology_data = QRSMorphologyData(ecg_lead, delineation, scale_id)

    r_zc_id = qrs_morphology_data.peak_zcs_ids[scale_id]
    q_zc_id = r_zc_id + q_zc_id_diff
    s_zc_id = r_zc_id + s_zc_id_diff

    if left_points:
        points = left_points + points
    onset_processing(q_zc_id, ecg_lead, delineation, qrs_morphology_data, points, -1)
    qrs_morphology_data = QRSMorphologyData(ecg_lead, delineation, scale_id)

    return points
