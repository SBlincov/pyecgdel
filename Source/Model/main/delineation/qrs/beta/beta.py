from Source.Model.main.delineation.qrs.beta.offset import define_qrs_offset_index
from Source.Model.main.delineation.qrs.beta.onset import define_qrs_onset_index
from Source.Model.main.delineation.qrs.beta.peak import define_qrs_peak_index
from Source.Model.main.delineation.wave_delineation import WaveDelineation


def get_qrs_delineation(ecg_lead, qrs_zc_id, qrs_zcs):

    delineation = WaveDelineation()

    # define qrs peak index for WaveDelineation instance
    define_qrs_peak_index(ecg_lead, delineation, qrs_zc_id, qrs_zcs)

    # define qrs onset index for WaveDelineation instance
    define_qrs_onset_index(ecg_lead, delineation, qrs_zc_id, qrs_zcs)

    # define qrs offset index for WaveDelineation instance
    define_qrs_offset_index(ecg_lead, delineation, qrs_zc_id, qrs_zcs)

    return delineation
