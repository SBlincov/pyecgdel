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

        rr_5_min = []

        num_complexes = len(qrs_dels)

        if len(qrs_dels) > 1:

            curr_rr_5_min = []

            id_5_min = 0

            for qrs_id in range(0, len(qrs_dels) - 1):
                current_rr = (qrs_dels[qrs_id + 1].peak_index - qrs_dels[qrs_id].peak_index) / rate
                rr_distribution.append(current_rr)

                if(qrs_dels[qrs_id + 1].peak_index < int((id_5_min + 1) * 300 * rate)):
                    curr_rr_5_min.append(current_rr)
                else:
                    rr_5_min.append(curr_rr_5_min)
                    curr_rr_5_min = []
                    id_5_min += 1

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
            qrs_characteristics.append([CharacteristicsNames.mean_rr, mean_rr])
            std_rr = np.std(rr_distribution)
            qrs_characteristics.append([CharacteristicsNames.std_rr, std_rr])

            # Regular
            mean_NN = mean_rr
            qrs_characteristics.append([CharacteristicsNames.mean_NN, mean_NN])
            max_sub_min_NN = np.max(rr_distribution) - np.min(rr_distribution)
            qrs_characteristics.append([CharacteristicsNames.max_sub_min_NN, max_sub_min_NN])

            # Statistics
            SDNN = std_rr
            qrs_characteristics.append([CharacteristicsNames.SDNN, SDNN])

            if len(signal) / rate < 43200: # 12 hours
                SDANN = SDNN
                SDNNindex = SDNN
            else:
                mean_5_min = []
                std_5_min = []
                for curr_5_min in rr_5_min:
                    curr_mean = np.mean(curr_5_min)
                    curr_std = np.std(curr_5_min)
                    mean_5_min.append(curr_mean)
                    std_5_min.append(curr_std)

                SDANN = np.std(mean_5_min)
                SDNNindex = np.mean(std_5_min)

            qrs_characteristics.append([CharacteristicsNames.SDANN, SDANN])
            qrs_characteristics.append([CharacteristicsNames.SDNNindex, SDNNindex])

            RMSSD = 0.0
            rr_diffs = []
            for rr_id in range(0, len(rr_distribution) - 1):
                rr_diffs.append((rr_distribution[rr_id + 1] - rr_distribution[rr_id]))
                RMSSD += pow((rr_distribution[rr_id + 1] - rr_distribution[rr_id]), 2.0)
            RMSSD = RMSSD / (len(rr_distribution) - 1)
            RMSSD = np.sqrt(RMSSD)

            qrs_characteristics.append([CharacteristicsNames.RMSSD, RMSSD])

            NN50 = 0
            for rr_diff in rr_diffs:
                if rr_diff > 0.05:
                    NN50 += 1
            pNN50 = NN50 / len(rr_diffs)

            qrs_characteristics.append([CharacteristicsNames.NN50, NN50])
            qrs_characteristics.append([CharacteristicsNames.pNN50, pNN50])

            # Geometry
            bins = np.arange(0.0, 3.0, 0.0078125).tolist()
            hist = np.histogram(rr_distribution, bins)
            triangular_index = np.max(hist[0]) / len(rr_distribution)
            qrs_characteristics.append([CharacteristicsNames.triangular_index, triangular_index])

        else:

            qrs_characteristics.append([CharacteristicsNames.mean_rr, 'n'])
            qrs_characteristics.append([CharacteristicsNames.std_rr, 'n'])

            # Regular
            qrs_characteristics.append([CharacteristicsNames.mean_NN, 'n'])
            qrs_characteristics.append([CharacteristicsNames.max_sub_min_NN, 'n'])

            # Statistics
            qrs_characteristics.append([CharacteristicsNames.SDNN, 'n'])
            qrs_characteristics.append([CharacteristicsNames.SDANN, 'n'])
            qrs_characteristics.append([CharacteristicsNames.SDNNindex, 'n'])
            qrs_characteristics.append([CharacteristicsNames.RMSSD, 'n'])
            qrs_characteristics.append([CharacteristicsNames.NN50, 'n'])
            qrs_characteristics.append([CharacteristicsNames.pNN50, 'n'])

            # Geometry
            qrs_characteristics.append([CharacteristicsNames.triangular_index, 'n'])


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
