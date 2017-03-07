"""
Фильтрация на основе непрерывного вейвлет-преобразования.
"""

from pycwt import *
from Source.Model.main.params.filter import FilterParams


def cwt_filtration(signal):
    mother_wavelet = wavelet.DOG(2)
    wave, scales, _, _, _, _ = wavelet.cwt(signal, 0.25, 0.25, 0.5, int(FilterParams['SCALE_COUNT']), mother_wavelet)

    for j in range(0, len(signal)):
        for i in range(0, int(FilterParams['LOW_LIMIT_SCALE_ID'])):
            wave[i][j] = 0.0

        for i in range(int(FilterParams['HIGH_LIMIT_SCALE_ID']), int(FilterParams['SCALE_COUNT'])):
            wave[i][j] = 0.0

    signal = wavelet.icwt(wave, scales, 0.25, 0.25, mother_wavelet)

    return signal

