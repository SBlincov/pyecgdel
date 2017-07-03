from Source.Model.main.zero_crossings.zero_crossing import *
from Source.Model.main.delineation.morfology_point import *


def r_processing(r_zc_id, ecg_lead, delineation, qrs_morphology_data, points, direction):
    scale_id = qrs_morphology_data.scale_id
    zcs = qrs_morphology_data.zcs[scale_id]

    r_zc_sign = qrs_morphology_data.r_signs[scale_id]

    r_index = zcs[r_zc_id].index
    r_value = ecg_lead.filtrated[r_index]
    if r_zc_sign is ExtremumSign.positive:
        r_sign = WaveSign.positive
    else:
        r_sign = WaveSign.negative
    r_point = Point(PointName.r, r_index, r_value, r_sign)
    if direction < 0:
        points.insert(0, r_point)
    else:
        points.append(r_point)

    delineation.peak_index = r_index


