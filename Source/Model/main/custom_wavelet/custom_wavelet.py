"""
Инициализация материнского вейвлета для дискретного вейвлет-преобразования.
"""

import pywt

# dec_lo = [1.0 / 128.0, 7.0 / 128.0, 21.0 / 128.0, 35.0 / 128.0, 35.0 / 128.0, 21.0 / 128.0, 7.0 / 128.0, 1.0 / 128.0]
# dec_hi = [0.0, 0.0, -2.0, 2.0, 0.0, 0.0, 0.0, 0.0]

dec_lo = [1.0 / 8.0, 3.0 / 8.0, 3.0 / 8.0, 1.0 / 8.0]
dec_hi = [0.0, -2.0, 2.0, 0.0]

rec_lo = dec_lo
rec_hi = dec_hi

filter_bank = [dec_lo, dec_hi, rec_lo, rec_hi]
CustomWavelet = pywt.Wavelet(name="CustomWavelet", filter_bank=filter_bank)
