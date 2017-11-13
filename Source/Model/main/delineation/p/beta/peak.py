from Source.Model.main.delineation.morfology_point import *
from Source.Model.main.zero_crossings.zero_crossing import *


def peak_processing(ecg_lead, delineation, morphology_data, points):

    direction = 0
    zcs = morphology_data.zcs
    peak_zc_id = morphology_data.peak_zc_id

    p_zc_sign = morphology_data.t_sign
    p_index = zcs[peak_zc_id].index
    p_value = ecg_lead.filter[p_index]
    if p_zc_sign == ExtremumSign.positive:
        p_sign = WaveSign.positive
    else:
        p_sign = WaveSign.negative
    p_point = Point(PointName.p_peak, p_index, p_value, p_sign)
    if direction < 0:
        points.insert(0, p_point)
    else:
        points.append(p_point)

    delineation.peak_index = p_index

