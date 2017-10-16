"""
Вычисление характеристик сигнала ЭКГ, связанных с волной T.
Данные характеристики используются в дальнейших подмодулях.
Вход: экземпляр класса отведения.
"""

from Source.Model.main.delineation.wave_delineation import *
from Source.Model.main.characteristics.characteristics_names import *
import numpy as np


def get_t_chars(lead):
    rate = lead.rate
    signal = lead.filter
    qrs_dels = lead.qrs_dels
    t_dels = lead.t_dels

    t_characteristics = []

    beat_num = 0
    if qrs_dels:
        beat_num += (len(qrs_dels) - 1)

    t_num = 0
    if t_dels:

        t_distribution = []
        qt_distribution = []
        st_distribution = []
        spec_distribution = []
        t_val_distribution = []

        t_num += len(t_dels)

        for t_id in range(0, len(t_dels)):
            t_distribution.append((t_dels[t_id].offset_index - t_dels[t_id].onset_index) / rate)
            spec_distribution.append(t_dels[t_id].specification)
            t_val_distribution.append(signal[t_dels[t_id].peak_index])

            qrs_id = t_id
            diff = t_dels[t_id].onset_index - qrs_dels[qrs_id].offset_index

            while diff > 0 and qrs_id < len(qrs_dels) - 1:
                qrs_id += 1
                diff = t_dels[t_id].onset_index - qrs_dels[qrs_id].offset_index
            qrs_id -= 1

            qt_distribution.append((t_dels[t_id].offset_index - qrs_dels[qrs_id].onset_index) / rate)

            s_index = qrs_dels[qrs_id].offset_index
            t_index = t_dels[t_id].onset_index
            st_distribution.append(signal[t_index] - signal[s_index])

        if beat_num > 0:
            presence_t = t_num / beat_num * 100.0
            t_characteristics.append([CharacteristicsNames.presence_t, presence_t])
        else:
            t_characteristics.append([CharacteristicsNames.presence_t, 'n'])

        if t_distribution:
            mean_t = np.mean(t_distribution)
            std_t = np.std(t_distribution)
            t_characteristics.append([CharacteristicsNames.mean_t, mean_t])
            t_characteristics.append([CharacteristicsNames.std_t, std_t])
        else:
            t_characteristics.append([CharacteristicsNames.mean_t, 'n'])
            t_characteristics.append([CharacteristicsNames.std_t, 'n'])

        if qt_distribution:
            mean_qt = np.mean(qt_distribution)
            std_qt = np.std(qt_distribution)
            t_characteristics.append([CharacteristicsNames.mean_qt, mean_qt])
            t_characteristics.append([CharacteristicsNames.std_qt, std_qt])
        else:
            t_characteristics.append([CharacteristicsNames.mean_qt, 'n'])
            t_characteristics.append([CharacteristicsNames.std_qt, 'n'])

        if st_distribution:
            mean_st = np.mean(st_distribution)
            std_st = np.std(st_distribution)
            t_characteristics.append([CharacteristicsNames.mean_st, mean_st])
            t_characteristics.append([CharacteristicsNames.std_st, std_st])
        else:
            t_characteristics.append([CharacteristicsNames.mean_st, 'n'])
            t_characteristics.append([CharacteristicsNames.std_st, 'n'])

        if spec_distribution:
            normal_t = float(spec_distribution.count(WaveSpecification.exist)) / float(len(spec_distribution)) * 100.0
            t_characteristics.append([CharacteristicsNames.normal_t, normal_t])
            flexure_t = float(spec_distribution.count(WaveSpecification.flexure)) / float(len(spec_distribution)) * 100.0
            t_characteristics.append([CharacteristicsNames.flexure_t, flexure_t])
            biphasic_t = float(spec_distribution.count(WaveSpecification.biphasic)) / float(len(spec_distribution)) * 100.0
            t_characteristics.append([CharacteristicsNames.biphasic_t, biphasic_t])
        else:
            t_characteristics.append([CharacteristicsNames.normal_t, 'n'])
            t_characteristics.append([CharacteristicsNames.flexure_t, 'n'])
            t_characteristics.append([CharacteristicsNames.biphasic_t, 'n'])

        if t_val_distribution:
            mean_t_val = np.mean(t_val_distribution)
            std_t_val = np.std(t_val_distribution)
            max_t_val = np.max(t_val_distribution)
            min_t_val = np.min(t_val_distribution)
            t_characteristics.append([CharacteristicsNames.mean_t_val, mean_t_val])
            t_characteristics.append([CharacteristicsNames.std_t_val, std_t_val])
            t_characteristics.append([CharacteristicsNames.max_t_val, max_t_val])
            t_characteristics.append([CharacteristicsNames.min_t_val, min_t_val])
        else:
            t_characteristics.append([CharacteristicsNames.mean_t_val, 'n'])
            t_characteristics.append([CharacteristicsNames.std_t_val, 'n'])
            t_characteristics.append([CharacteristicsNames.max_t_val, 'n'])
            t_characteristics.append([CharacteristicsNames.min_t_val, 'n'])

    return t_characteristics
