"""
Алгорим поиска пика T.

Входные параметры:
    ecg_lead - экземпляр класса отведения сигнала ЭКГ.
    qrs_id - индекс текущего комплекса QRS.
    zcs - список пересечений нуля детализирующими вейвлет-коэффициентами.
    peak_zc_id - индекс пересечения нуля, соотвествующий пику комплекса.
"""

from Source.Model.main.params.t import *
from Source.Model.main.ecg_lead.ecg_lead import *
from Source.Model.main.modulus_maxima.routines import *
from Source.Model.main.delineation.t.routines import *


def get_t_peak_zc_id(ecg_lead, qrs_id, zcs):

    begin_index = get_t_begin_index(ecg_lead, qrs_id)
    end_index = get_t_end_index(ecg_lead, qrs_id)

    # Shifting from borders
    zcs_peaks_candidates_begin_index = zcs[0].index - (zcs[0].index - begin_index) * float(TParams['ALPHA_PEAK_ZC_AMPL_DEC_LEFT'])
    zcs_peaks_candidates_end_index = zcs[-1].index + (end_index - zcs[-1].index) * float(TParams['ALPHA_PEAK_ZC_AMPL_DEC_RIGHT'])
    zcs_peaks_candidates_window = zcs_peaks_candidates_end_index - zcs_peaks_candidates_begin_index

    begin_part = float(TParams['ALPHA_PEAK_ZC_AMPL_DEC_BEGIN'])
    end_part = 1.0 - begin_part
    zcs_peaks_candidates_point = zcs_peaks_candidates_begin_index + zcs_peaks_candidates_window * begin_part

    peak_zc_id = 0
    peak_zc_mm_amplitude = 0.0

    for candidate_zc_id in range(len(zcs)):

        shift_percentage = float(zcs[candidate_zc_id].index - zcs_peaks_candidates_point)
        if shift_percentage < 0.0:
            shift_percentage = abs(shift_percentage) / (zcs_peaks_candidates_window * begin_part)
        else:
            shift_percentage = abs(shift_percentage) / (zcs_peaks_candidates_window * end_part)

        amplitude_part = 1.0 - pow(shift_percentage, float(TParams['ALPHA_PEAK_ZC_AMPL_DEC_POW'])) * float(TParams['ALPHA_PEAK_ZC_AMPL_DEC_COEFF'])

        if zcs[candidate_zc_id].mm_amplitude * amplitude_part >= peak_zc_mm_amplitude:
            peak_zc_id = candidate_zc_id
            peak_zc_mm_amplitude = zcs[candidate_zc_id].mm_amplitude * amplitude_part

    return peak_zc_id
