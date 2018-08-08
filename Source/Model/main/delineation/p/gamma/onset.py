from Source.Model.main.delineation.morfology_point import *


def onset_processing(ecg_lead, delineation, morphology_data, points):

    onset_index = delineation.onset_index
    onset_value = ecg_lead.filter[onset_index]
    onset_sign = WaveSign.none
    onset_point = Point(PointName.p_onset, onset_index, onset_value, onset_sign)
    points.insert(0, onset_point)

    delineation.onset_index = onset_index
