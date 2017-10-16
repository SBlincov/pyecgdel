from Source.Model.main.delineation.t.routines import get_t_wdc_scale_id
from Source.Model.main.delineation.t.beta.data import TMorphologyData
from Source.Model.main.params.t import TParams
from Source.Model.main.delineation.wave_delineation import *
from Source.Model.main.delineation.morfology_point import *
from Source.Model.main.zero_crossings.zero_crossing import *


def onset_processing(ecg_lead, delineation, t_morphology_data, points):

    onset_index = delineation.onset_index
    onset_value = ecg_lead.filter[onset_index]
    onset_sign = WaveSign.none
    onset_point = Point(PointName.t_onset, onset_index, onset_value, onset_sign)
    points.insert(0, onset_point)

    delineation.onset_index = onset_index
