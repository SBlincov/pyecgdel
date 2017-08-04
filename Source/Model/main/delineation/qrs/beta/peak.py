"""
Алгорим поиска пика QRS.

Входные параметры:
    ecg_lead - экземпляр класса отведения сигнала ЭКГ.
    delineation - экземпляр класса, содержащего информацию о текущем сегментированном комплексе.
    qrs_zc_id - индекс пересечения нуля детализирующими вейвлет-коэффициентами для текущего комплекса QRS.
    qrs_zcs - список пересечений нуля детализирующими вейвлет-коэффициентами.
"""

from Source.Model.main.delineation.wave_delineation import *


def define_qrs_peak_index(ecg_lead, delineation, qrs_zc):

    qrs_peak_index = qrs_zc.index
    delineation.peak_index = qrs_peak_index
    delineation.specification = WaveSpecification.normal

