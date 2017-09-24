from Source.Model.main.delineation.t.routines import get_t_wdc_scale_id
from Source.Model.main.delineation.t.beta.data import TMorphologyData
from Source.Model.main.params.t import TParams
from Source.Model.main.delineation.wave_delineation import *
from Source.Model.main.delineation.morfology_point import *
from Source.Model.main.zero_crossings.zero_crossing import *


def xtd_processing(ecg_lead, delineation, t_morphology_data, points):

    zcs = t_morphology_data.zcs
    peak_zc_id = t_morphology_data.peak_zc_id

    if peak_zc_id > 0:
        xtd_pre_points = []
        for zc_id in range(0, peak_zc_id):
            p_index = zcs[zc_id].index
            p_value = ecg_lead.filtrated[p_index]
            if zcs[zc_id].extremum_sign is ExtremumSign.negative:
                p_sign = WaveSign.negative
            else:
                p_sign = WaveSign.positive
            p = Point(PointName.xtd_point, p_index, p_value, p_sign)
            xtd_pre_points.append(p)

        points = xtd_pre_points + points

    if peak_zc_id < len(zcs) - 1:
        xtd_post_points = []
        for zc_id in range(peak_zc_id, len(zcs)):
            p_index = zcs[zc_id].index
            p_value = ecg_lead.filtrated[p_index]
            if zcs[zc_id].extremum_sign is ExtremumSign.negative:
                p_sign = WaveSign.negative
            else:
                p_sign = WaveSign.positive
            p = Point(PointName.xtd_point, p_index, p_value, p_sign)
            xtd_post_points.append(p)

        points = points + xtd_post_points
