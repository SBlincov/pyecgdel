from Source.Model.main.delineation.t.routines import get_t_wdc_scale_id
from Source.Model.main.delineation.t.beta.data import TMorphologyData
from Source.Model.main.params.t import TParams
from Source.Model.main.delineation.wave_delineation import *
from Source.Model.main.delineation.morfology_point import *
from Source.Model.main.zero_crossings.zero_crossing import *


def offset_processing(ecg_lead, delineation, t_morphology_data, points):
    offset_index = delineation.offset_index
    offset_value = ecg_lead.filter[offset_index]
    offset_sign = WaveSign.none
    offset_point = Point(PointName.t_offset, offset_index, offset_value, offset_sign)
    points.append(offset_point)

    delineation.offset_index = offset_index
