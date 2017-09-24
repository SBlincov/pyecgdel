from Source.Model.main.delineation.t.routines import get_t_wdc_scale_id
from Source.Model.main.delineation.t.beta.data import TMorphologyData
from Source.Model.main.params.t import TParams
from Source.Model.main.delineation.wave_delineation import *
from Source.Model.main.delineation.morfology_point import *
from Source.Model.main.zero_crossings.zero_crossing import *
from Source.Model.main.delineation.t.beta.peak import peak_processing
from Source.Model.main.delineation.t.beta.xtd import xtd_processing
from Source.Model.main.delineation.t.beta.onset import onset_processing
from Source.Model.main.delineation.t.beta.offset import offset_processing


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

