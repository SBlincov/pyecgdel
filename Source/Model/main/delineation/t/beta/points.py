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

