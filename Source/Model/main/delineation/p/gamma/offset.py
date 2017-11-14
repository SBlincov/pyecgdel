from Source.Model.main.delineation.morfology_point import *


def offset_processing(ecg_lead, delineation, morphology_data, points):
    offset_index = delineation.offset_index
    offset_value = ecg_lead.filter[offset_index]
    offset_sign = WaveSign.none
    offset_point = Point(PointName.p_offset, offset_index, offset_value, offset_sign)
    points.append(offset_point)

    delineation.offset_index = offset_index
