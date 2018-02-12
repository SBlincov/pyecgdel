from Source.Model.main.delineation.qrs.beta.offset import define_qrs_offset_index
from Source.Model.main.delineation.qrs.beta.onset import define_qrs_onset_index
from Source.Model.main.delineation.qrs.beta.peak import define_qrs_peak_index
from Source.Model.main.delineation.wave_delineation import WaveDelineation


def beta_processing(ecg_lead, qrs_zc):

    delineation = WaveDelineation()

    # define qrs peak index for WaveDelineation instance
    define_qrs_peak_index(ecg_lead, delineation, qrs_zc)

    # define qrs onset index for WaveDelineation instance
    define_qrs_onset_index(ecg_lead, delineation, qrs_zc)

    # define qrs offset index for WaveDelineation instance
    define_qrs_offset_index(ecg_lead, delineation, qrs_zc)

    return delineation
