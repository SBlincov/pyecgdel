"""
Вычисление характеристик сигнала ЭКГ, связанных с комплексом QRS.
Данные характеристики используются в дальнейших подмодулях.
Вход: экземпляр класса отведения.
"""

from Source.Model.main.delineation.wave_delineation import *
from Source.Model.main.characteristics.characteristics_names import *
import numpy as np


def get_qrs_chars(lead):

    sampling_rate = lead.sampling_rate
    signal = lead.filtrated
    qrs_dels = lead.qrs_dels

    qrs_characteristics = []

    if qrs_dels:

        rr_distribution = []
        qrs_distribution = []
        spec_distribution = []
        r_val_distribution = []

        for qrs_seq in qrs_dels:

            if len(qrs_seq) > 1:

                for qrs_id in range(0, len(qrs_seq) - 1):
                    current_rr = (qrs_seq[qrs_id + 1].peak_index - qrs_seq[qrs_id].peak_index) / sampling_rate
                    rr_distribution.append(current_rr)
                    current_qrs = (qrs_seq[qrs_id].offset_index - qrs_seq[qrs_id].onset_index) / sampling_rate
                    qrs_distribution.append(current_qrs)
                    spec_distribution.append(qrs_seq[qrs_id].specification)
                    r_val_distribution.append(signal[qrs_seq[qrs_id].peak_index])

                current_qrs = (qrs_seq[len(qrs_seq) - 1].offset_index - qrs_seq[len(qrs_seq) - 1].onset_index) / sampling_rate
                qrs_distribution.append(current_qrs)
                spec_distribution.append(qrs_seq[len(qrs_seq) - 1].specification)
                r_val_distribution.append(signal[qrs_seq[len(qrs_seq) - 1].peak_index])

        if rr_distribution:
            mean_rr = np.mean(rr_distribution)
            std_rr = np.std(rr_distribution)
            qrs_characteristics.append([CharacteristicsNames.mean_rr, mean_rr])
            qrs_characteristics.append([CharacteristicsNames.std_rr, std_rr])
        else:
            qrs_characteristics.append([CharacteristicsNames.mean_rr, 'n'])
            qrs_characteristics.append([CharacteristicsNames.std_rr, 'n'])

        if qrs_distribution:
            mean_qrs = np.mean(qrs_distribution)
            std_qrs = np.std(qrs_distribution)
            qrs_characteristics.append([CharacteristicsNames.mean_qrs, mean_qrs])
            qrs_characteristics.append([CharacteristicsNames.std_qrs, std_qrs])
        else:
            qrs_characteristics.append([CharacteristicsNames.mean_qrs, 'n'])
            qrs_characteristics.append([CharacteristicsNames.std_qrs, 'n'])

        if spec_distribution:
            normal_qrs = float(spec_distribution.count(WaveSpecification.exist)) / float(len(spec_distribution)) * 100.0
            qrs_characteristics.append([CharacteristicsNames.normal_qrs, normal_qrs])
            flexure_qrs = float(spec_distribution.count(WaveSpecification.flexure)) / float(len(spec_distribution)) * 100.0
            qrs_characteristics.append([CharacteristicsNames.flexure_qrs, flexure_qrs])
            extra_qrs = float(spec_distribution.count(WaveSpecification.extra)) / float(len(spec_distribution)) * 100.0
            qrs_characteristics.append([CharacteristicsNames.extra_qrs, extra_qrs])
        else:
            qrs_characteristics.append([CharacteristicsNames.normal_qrs, 'n'])
            qrs_characteristics.append([CharacteristicsNames.flexure_qrs, 'n'])
            qrs_characteristics.append([CharacteristicsNames.extra_qrs, 'n'])

        if r_val_distribution:
            mean_r_val = np.mean(r_val_distribution)
            std_r_val = np.std(r_val_distribution)
            max_r_val = np.max(r_val_distribution)
            min_r_val = np.min(r_val_distribution)
            qrs_characteristics.append([CharacteristicsNames.mean_r_val, mean_r_val])
            qrs_characteristics.append([CharacteristicsNames.std_r_val, std_r_val])
            qrs_characteristics.append([CharacteristicsNames.max_r_val, max_r_val])
            qrs_characteristics.append([CharacteristicsNames.min_r_val, min_r_val])
        else:
            qrs_characteristics.append([CharacteristicsNames.mean_r_val, 'n'])
            qrs_characteristics.append([CharacteristicsNames.std_r_val, 'n'])
            qrs_characteristics.append([CharacteristicsNames.max_r_val, 'n'])
            qrs_characteristics.append([CharacteristicsNames.min_r_val, 'n'])

    return qrs_characteristics









