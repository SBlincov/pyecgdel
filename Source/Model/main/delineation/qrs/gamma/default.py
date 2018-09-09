from Source.Model.main.zero_crossings.zero_crossing import *
from Source.Model.main.delineation.morfology_point import *


def processing_default_morphology(ecg_lead, delineation, morph_data):

    points = []

    scale_id = morph_data.scale_id
    zcs = morph_data.zcs[scale_id]
    peak_zc_id = morph_data.peak_zcs_ids[scale_id]

    onset_index = delineation.onset_index
    offset_index = delineation.offset_index

    qrs_onset_index = onset_index
    qrs_onset_value = ecg_lead.filter[qrs_onset_index]
    qrs_onset_sign = WaveSign.none
    qrs_onset_point = Point(PointName.qrs_onset, qrs_onset_index, qrs_onset_value, qrs_onset_sign)
    points.insert(0, qrs_onset_point)

    r_index = zcs[peak_zc_id].index
    r_value = ecg_lead.filter[r_index]
    if zcs[peak_zc_id].extremum_sign is ExtremumSign.negative:
        r_sign = WaveSign.negative
    else:
        r_sign = WaveSign.positive
    r_point = Point(PointName.r, r_index, r_value, r_sign)
    points.append(r_point)

    qrs_offset_index = offset_index
    qrs_offset_value = ecg_lead.filter[qrs_offset_index]
    qrs_offset_sign = WaveSign.none
    qrs_offset_point = Point(PointName.qrs_offset, qrs_offset_index, qrs_offset_value, qrs_offset_sign)
    points.append(qrs_offset_point)

    return points
