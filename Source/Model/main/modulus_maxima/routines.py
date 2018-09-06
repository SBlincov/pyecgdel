"""
Вспомогательные фукнции для поиска экстремумов детализирующих вейвлет-коэффициентов.
"""

from Source.Model.main.modulus_maxima.modulus_maxima import ModulusMaxima
from scipy.signal import argrelextrema
import numpy as np

def get_mms(wdc):
    mins = argrelextrema(wdc, np.less)[0]
    maxs = argrelextrema(wdc, np.greater)[0]
    peaks = np.sort(np.concatenate([mins, maxs]))
    mms = []
    for id in range(0, len(peaks)):
        peak = peaks[id]
        mm = ModulusMaxima(peak, id, wdc)
        mms.append(mm)
    return mms


