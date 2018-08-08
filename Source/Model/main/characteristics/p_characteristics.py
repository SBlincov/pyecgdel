"""
Вычисление характеристик сигнала ЭКГ, связанных с волной P.
Данные характеристики используются в дальнейших подмодулях.
Вход: экземпляр класса отведения.
"""

from ..delineation.wave_delineation import *
from .characteristics_names import *
from Source.Model.main.delineation.morfology_point import *
import numpy as np


def get_p_chars(lead):
    rate = lead.rate
    signal = lead.filter
    qrs_dels = lead.qrs_dels
    p_dels = lead.p_dels
    p_morphs = lead.p_morphs

    p_characteristics = []

    beat_num = 0
    if qrs_dels:
        beat_num += (len(qrs_dels) - 1)

    p_num = len(p_dels)

    if p_dels:

        p_distribution = []
        pq_distribution = []
        spec_distribution = []
        p_val_distribution = []

        points_global = []
        num_xtd_points_global = []

        for p_id in range(0, len(p_dels)):
            p_distribution.append((p_dels[p_id].offset_index - p_dels[p_id].onset_index) / rate)
            spec_distribution.append(p_dels[p_id].specification)
            p_val_distribution.append(signal[p_dels[p_id].peak_index])

            qrs_id = p_id
            diff = qrs_dels[qrs_id].onset_index - p_dels[p_id].offset_index

            while diff < 0 and qrs_id < len(qrs_dels) - 1:
                qrs_id += 1
                diff = qrs_dels[qrs_id].onset_index - p_dels[p_id].offset_index

            pq_distribution.append((qrs_dels[qrs_id].onset_index - p_dels[p_id].onset_index) / rate)

            points_global.append(p_morphs[p_id].points)

            num_xtd_points = 0
            for point in p_morphs[p_id].points:
                if point.name is PointName.xtd_point:
                    num_xtd_points += 1
            num_xtd_points_global.append(num_xtd_points)

        if beat_num > 0:
            presence_p = p_num / beat_num * 100.0
            p_characteristics.append([CharacteristicsNames.presence_p, float(presence_p)])
        else:
            p_characteristics.append([CharacteristicsNames.presence_p, 'n'])

        if p_distribution:
            mean_p = np.mean(p_distribution)
            std_p = np.std(p_distribution)
            p_characteristics.append([CharacteristicsNames.mean_p, float(mean_p)])
            p_characteristics.append([CharacteristicsNames.std_p, float(std_p)])
        else:
            p_characteristics.append([CharacteristicsNames.mean_p, 'n'])
            p_characteristics.append([CharacteristicsNames.std_p, 'n'])

        if pq_distribution:
            mean_pq = np.mean(pq_distribution)
            std_pq = np.std(pq_distribution)
            p_characteristics.append([CharacteristicsNames.mean_pq, float(mean_pq)])
            p_characteristics.append([CharacteristicsNames.std_pq, float(std_pq)])
        else:
            p_characteristics.append([CharacteristicsNames.mean_pq, 'n'])
            p_characteristics.append([CharacteristicsNames.std_pq, 'n'])

        if spec_distribution:

            num_normal = 0
            num_flexure = 0
            for p_id in range(0, len(p_dels)):
                num_xtd_points = num_xtd_points_global[p_id]
                if p_dels[p_id].specification is not WaveSpecification.biphasic:
                    if num_xtd_points == 0:
                        num_normal += 1
                    else:
                        num_flexure += 1

            normal_p = float(num_normal) / float(p_num) * 100.0
            p_characteristics.append([CharacteristicsNames.normal_p, float(normal_p)])

            flexure_p = float(num_flexure) / float(p_num) * 100.0
            p_characteristics.append([CharacteristicsNames.flexure_p, float(flexure_p)])

            biphasic_p = float(spec_distribution.count(WaveSpecification.biphasic)) / float(p_num) * 100.0
            p_characteristics.append([CharacteristicsNames.biphasic_p, float(biphasic_p)])

            atrial_fibrillation_p = float(spec_distribution.count(WaveSpecification.atrial_fibrillation)) / float(p_num) * 100.0
            p_characteristics.append([CharacteristicsNames.atrial_fibrillation_p, float(atrial_fibrillation_p)])

        else:
            p_characteristics.append([CharacteristicsNames.normal_p, 'n'])
            p_characteristics.append([CharacteristicsNames.flexure_p, 'n'])
            p_characteristics.append([CharacteristicsNames.biphasic_p, 'n'])
            p_characteristics.append([CharacteristicsNames.atrial_fibrillation_p, 'n'])

        if p_val_distribution:
            mean_p_val = np.mean(p_val_distribution)
            std_p_val = np.std(p_val_distribution)
            max_p_val = np.max(p_val_distribution)
            min_p_val = np.min(p_val_distribution)
            p_characteristics.append([CharacteristicsNames.mean_p_val, float(mean_p_val)])
            p_characteristics.append([CharacteristicsNames.std_p_val, float(std_p_val)])
            p_characteristics.append([CharacteristicsNames.max_p_val, float(max_p_val)])
            p_characteristics.append([CharacteristicsNames.min_p_val, float(min_p_val)])
        else:
            p_characteristics.append([CharacteristicsNames.mean_p_val, 'n'])
            p_characteristics.append([CharacteristicsNames.std_p_val, 'n'])
            p_characteristics.append([CharacteristicsNames.max_p_val, 'n'])
            p_characteristics.append([CharacteristicsNames.min_p_val, 'n'])

    else:

        p_characteristics.append([CharacteristicsNames.presence_p, 0.0])
        p_characteristics.append([CharacteristicsNames.mean_p, 'n'])
        p_characteristics.append([CharacteristicsNames.std_p, 'n'])
        p_characteristics.append([CharacteristicsNames.mean_pq, 'n'])
        p_characteristics.append([CharacteristicsNames.std_pq, 'n'])
        p_characteristics.append([CharacteristicsNames.normal_p, 'n'])
        p_characteristics.append([CharacteristicsNames.flexure_p, 'n'])
        p_characteristics.append([CharacteristicsNames.biphasic_p, 'n'])
        p_characteristics.append([CharacteristicsNames.atrial_fibrillation_p, 'n'])
        p_characteristics.append([CharacteristicsNames.mean_p_val, 'n'])
        p_characteristics.append([CharacteristicsNames.std_p_val, 'n'])
        p_characteristics.append([CharacteristicsNames.max_p_val, 'n'])
        p_characteristics.append([CharacteristicsNames.min_p_val, 'n'])

    return p_characteristics
