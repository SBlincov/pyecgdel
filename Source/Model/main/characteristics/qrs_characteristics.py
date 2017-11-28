"""
Вычисление характеристик сигнала ЭКГ, связанных с комплексом QRS.
Данные характеристики используются в дальнейших подмодулях.
Вход: экземпляр класса отведения.
"""

from Source.Model.main.delineation.wave_delineation import *
from Source.Model.main.characteristics.characteristics_names import *
from Source.Model.main.delineation.morfology_point import *
import numpy as np


def get_qrs_chars(lead):
    rate = lead.rate
    signal = lead.filter
    qrs_dels = lead.qrs_dels
    qrs_morphs = lead.qrs_morphs

    qrs_characteristics = []

    if qrs_dels:

        rr_distribution = []
        qrs_distribution = []
        spec_distribution = []
        r_val_distribution = []

        points_global = []
        num_xtd_points_global = []

        num_complexes = len(qrs_dels)

        if len(qrs_dels) > 1:

            for qrs_id in range(0, len(qrs_dels) - 1):
                current_rr = (qrs_dels[qrs_id + 1].peak_index - qrs_dels[qrs_id].peak_index) / rate
                rr_distribution.append(current_rr)

                current_qrs = (qrs_dels[qrs_id].offset_index - qrs_dels[qrs_id].onset_index) / rate
                qrs_distribution.append(current_qrs)
                spec_distribution.append(qrs_dels[qrs_id].specification)
                r_val_distribution.append(signal[qrs_dels[qrs_id].peak_index])

                points_global.append(qrs_morphs[qrs_id].points)

                num_xtd_points = 0
                for point in qrs_morphs[qrs_id].points:
                    if point.name is PointName.xtd_point:
                        num_xtd_points += 1
                num_xtd_points_global.append(num_xtd_points)

            current_qrs = (qrs_dels[len(qrs_dels) - 1].offset_index - qrs_dels[len(qrs_dels) - 1].onset_index) / rate
            qrs_distribution.append(current_qrs)
            spec_distribution.append(qrs_dels[len(qrs_dels) - 1].specification)
            r_val_distribution.append(signal[qrs_dels[len(qrs_dels) - 1].peak_index])

            points_global.append(qrs_morphs[len(qrs_dels) - 1].points)

            num_xtd_points = 0
            for point in qrs_morphs[len(qrs_dels) - 1].points:
                if point.name is PointName.xtd_point:
                    num_xtd_points += 1
            num_xtd_points_global.append(num_xtd_points)

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

            num_normal_qrs = 0
            num_flexure_qrs = 0
            for num_xtd_points in num_xtd_points_global:
                if num_xtd_points == 0:
                    num_normal_qrs += 1
                else:
                    num_flexure_qrs += 1

            normal_qrs = float(num_normal_qrs) / float(num_complexes) * 100.0
            qrs_characteristics.append([CharacteristicsNames.normal_qrs, normal_qrs])

            flexure_qrs = float(num_flexure_qrs) / float(num_complexes) * 100.0
            qrs_characteristics.append([CharacteristicsNames.flexure_qrs, flexure_qrs])

            extra_qrs = float(spec_distribution.count(WaveSpecification.extra)) / float(num_complexes) * 100.0
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

    else:

        qrs_characteristics.append([CharacteristicsNames.mean_rr, 'n'])
        qrs_characteristics.append([CharacteristicsNames.std_rr, 'n'])
        qrs_characteristics.append([CharacteristicsNames.mean_qrs, 'n'])
        qrs_characteristics.append([CharacteristicsNames.std_qrs, 'n'])
        qrs_characteristics.append([CharacteristicsNames.normal_qrs, 'n'])
        qrs_characteristics.append([CharacteristicsNames.flexure_qrs, 'n'])
        qrs_characteristics.append([CharacteristicsNames.extra_qrs, 'n'])
        qrs_characteristics.append([CharacteristicsNames.mean_r_val, 'n'])
        qrs_characteristics.append([CharacteristicsNames.std_r_val, 'n'])
        qrs_characteristics.append([CharacteristicsNames.max_r_val, 'n'])
        qrs_characteristics.append([CharacteristicsNames.min_r_val, 'n'])

    return qrs_characteristics
