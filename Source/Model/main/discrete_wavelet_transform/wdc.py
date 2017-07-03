"""
Вычисление детализирующих вейвлет-коэффициентов.

Входные параметры:
    signal - сигнал ЭКГ.
"""

import pywt
import numpy as np
from Source.Model.main.custom_wavelet.custom_wavelet import CustomWavelet
from Source.Infrastructure.main.config import *


def get_wdc(signal):

    num_dwt_scales = int(ConfigParams['NUM_WDC_SCALES'])
    dwt_segment = pow(2, num_dwt_scales)
    dwt_shift = len(signal) % dwt_segment
    if dwt_shift != 0:
        signal = signal[0:len(signal) - dwt_shift]

    max_decomposition_level = pywt.swt_max_level(len(signal))
    custom_wavelet = CustomWavelet
    # custom_wavelet = pywt.Wavelet('coif1')
    coeffs = pywt.swt(signal, custom_wavelet, level=num_dwt_scales, start_level=0)

    wdc = []

    wdc_shifts = [0, 1, 3, 7, 15, 31, 65]

    for scale_id in range(0, num_dwt_scales):
        wdc_current_scale = coeffs[num_dwt_scales - 1 - scale_id][1]
        if scale_id > 0:
            list_of_zeros = np.asarray([0] * wdc_shifts[scale_id])
            wdc_current_scale = wdc_current_scale[0:-wdc_shifts[scale_id]]
            wdc_current_scale = np.concatenate((list_of_zeros, wdc_current_scale))
        wdc.append(wdc_current_scale)

    return wdc

