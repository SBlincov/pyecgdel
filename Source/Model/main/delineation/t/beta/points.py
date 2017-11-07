from Source.Model.main.delineation.t.beta.peak import peak_processing
from Source.Model.main.delineation.t.beta.xtd import xtd_processing
from Source.Model.main.delineation.t.beta.onset import onset_processing
from Source.Model.main.delineation.t.beta.offset import offset_processing
from Source.Model.main.delineation.morfology_point import *


def points_processing(ecg_lead, delineation, t_morphology_data):

    points = []

    # Firstly get T-peak
    peak_processing(ecg_lead, delineation, t_morphology_data, points)

    # Get all xtd peaks
    xtd_processing(ecg_lead, delineation, t_morphology_data, points)

    # Get onset
    onset_processing(ecg_lead, delineation, t_morphology_data, points)

    # Get offset
    offset_processing(ecg_lead, delineation, t_morphology_data, points)

    return points


def points_processing_trivial(ecg_lead, delineation):

    onset_name = PointName.t_onset
    onset_index = delineation.onset_index
    onset_value = ecg_lead.filter[onset_index]
    onset_sign = WaveSign.none
    onset = Point(onset_name, onset_index, onset_value, onset_sign)

    offset_name = PointName.t_offset
    offset_index = delineation.offset_index
    offset_value = ecg_lead.filter[offset_index]
    offset_sign = WaveSign.none
    offset = Point(offset_name, offset_index, offset_value, offset_sign)

    peak_name = PointName.t_peak
    peak_index = delineation.peak_index
    peak_value = ecg_lead.filter[peak_index]

    # if we have Line[{x1, y1}, {x2, y2}] and Point {xA, yA}
    # first vector v1 = {x2 - x1, y2 - y1}
    # second vector v2 = {x2 - xA, y2 - yA}
    # cross product xp = v1.x * v2.y - v1.y * v2.x

    cross_prod = (offset_index - onset_index) * (offset_value - peak_value) - \
                 (offset_value - onset_value) * (offset_index - peak_index)

    if cross_prod > 0:
        peak_sign = WaveSign.positive
    elif cross_prod < 0:
        peak_sign = WaveSign.negative
    else:
        peak_sign = WaveSign.none

    peak = Point(peak_name, peak_index, peak_value, peak_sign)

    points = [onset, peak, offset]

    return points
