from Source.Model.main.delineation.t.routines import get_t_wdc_scale_id
from Source.Model.main.delineation.t.beta.data import TMorphologyData
from Source.Model.main.params.t import TParams
from Source.Model.main.delineation.wave_delineation import *
from Source.Model.main.delineation.morfology_point import *
from Source.Model.main.zero_crossings.zero_crossing import *


def peak_processing(ecg_lead, delineation, t_morphology_data, points):

    direction = 0
    zcs = t_morphology_data.zcs
    peak_zc_id = t_morphology_data.peak_zc_id

    t_zc_sign = t_morphology_data.t_sign
    t_index = zcs[peak_zc_id].index
    t_value = ecg_lead.filtrated[t_index]
    if t_zc_sign == ExtremumSign.positive:
        t_sign = WaveSign.positive
    else:
        t_sign = WaveSign.negative
    t_point = Point(PointName.t_peak, t_index, t_value, t_sign)
    if direction < 0:
        points.insert(0, t_point)
    else:
        points.append(t_point)

    delineation.peak_index = t_index

