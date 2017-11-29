"""
Вычисление характеристик сигнала ЭКГ, связанных с комплексом QRS.
Данные характеристики используются в дальнейших подмодулях.
Вход: экземпляр класса отведения.
"""

from Source.Model.main.delineation.wave_delineation import *
from Source.Model.main.characteristics.characteristics_names import *
from Source.Model.main.delineation.morfology_point import *
import numpy as np


def get_global_chars(ecg):

    leads = ecg.leads

    qrs_chars = []
    rr_distribution = []
    for lead in leads:

        rate = lead.rate
        qrs_dels = lead.qrs_dels

        if qrs_dels:

            rr_dist_curr = []

            num_complexes = len(qrs_dels)

            if len(qrs_dels) > 1:

                for qrs_id in range(0, len(qrs_dels) - 1):
                    current_rr = (qrs_dels[qrs_id + 1].peak_index - qrs_dels[qrs_id].peak_index) / rate
                    rr_dist_curr.append(current_rr)

            rr_distribution.append(rr_dist_curr)

        return qrs_chars
