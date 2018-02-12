from Source.Model.main.delineation.morfology_point import *
from Source.Model.main.zero_crossings.zero_crossing import *


def xtd_processing(ecg_lead, delineation, morphology_data, points):

    zcs = morphology_data.zcs
    peak_zc_id = morphology_data.peak_zc_id

    if peak_zc_id > 0:
        for zc_id in range(peak_zc_id - 1, -1, -1):
            p_index = zcs[zc_id].index
            p_value = ecg_lead.filter[p_index]
            if zcs[zc_id].extremum_sign is ExtremumSign.negative:
                p_sign = WaveSign.negative
            else:
                p_sign = WaveSign.positive
            p = Point(PointName.xtd_point, p_index, p_value, p_sign)
            points.insert(0, p)

    if peak_zc_id < len(zcs) - 1:
        for zc_id in range(peak_zc_id + 1, len(zcs)):
            p_index = zcs[zc_id].index
            p_value = ecg_lead.filter[p_index]
            if zcs[zc_id].extremum_sign is ExtremumSign.negative:
                p_sign = WaveSign.negative
            else:
                p_sign = WaveSign.positive
            p = Point(PointName.xtd_point, p_index, p_value, p_sign)
            points.append(p)
