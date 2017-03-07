"""
Фильтрация на основе полосовых фильтров
"""

from scipy.signal import butter, lfilter


def butter_bandpass(low_cut, high_cut, fs, order=5):
    nyq = 0.5 * fs
    low = low_cut / nyq
    high = high_cut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, low_cut, high_cut, fs, order=5):
    b, a = butter_bandpass(low_cut, high_cut, fs, order=order)
    y = lfilter(b, a, data)
    return y


def common_filtration(ecg_lead, low_cut=0.3, high_cut=80.0, order=5):
    signal = ecg_lead.signal
    sampling_rate = ecg_lead.sampling_rate
    signal = butter_bandpass_filter(signal, low_cut, high_cut, sampling_rate, order)
    return signal





