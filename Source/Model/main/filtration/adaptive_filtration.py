"""
Адаптивная фильтрация на основе полосовых фильтров, фильтра Savitzky-Golay и с испльзованием сегментации
"""

from scipy.signal import butter, savgol_filter, filtfilt


def _filter_sg(signal, order):
    return savgol_filter(signal, 11, order)

def _butter_highpass(data, low_cut, fs, order):
    nyq = 0.5 * fs
    low = low_cut / nyq
    b, a = butter(order, low, btype='highpass')
    return filtfilt(b, a, data, method='gust')

# Return weights for linear combination of base_signal and smoothed
def _get_weights(ecg_lead, base_signal, smooth_signal):
    weights = [0.0] * len(base_signal)
    # Do not apply filtering at QRS areas
    for delineation in ecg_lead.qrs_dels:
        for idx in range(int(delineation.onset_index), int(delineation.offset_index)):
            weights[idx] = 1.0
    threshold_diff_mkv = 50.0
    for idx in range(0, len(base_signal)):
        if abs(base_signal[idx] - smooth_signal[idx]) > threshold_diff_mkv:
            weights[idx] = 1.0
    for idx in range(0, len(weights)):
        window_size = 10
        if weights[idx] == 1.0:
            for i in range(max(idx - window_size, 0), idx):
                weights[i] = max(weights[i], 1.0 - abs(idx - i) / float(window_size))
            for i in range(idx, min(idx + window_size, len(weights))):
                weights[i] = max(weights[i], 1.0 - abs(i - idx) / float(window_size))
    return weights


def adaptive_filtration(ecg_lead, low_cut=0.35, order=3):
    signal = ecg_lead.origin
    sampling_rate = ecg_lead.rate
    # filter out (most of) baseline drift and use it as base
    base_signal = _butter_highpass(signal, low_cut, sampling_rate, order)
    # filter out high frequences
    smooth_signal = _filter_sg(base_signal, order)
    # combine base and smooth signals
    weights_base = _get_weights(ecg_lead, base_signal, smooth_signal)
    filtered = smooth_signal
    for idx in range(0, len(base_signal)):
        filtered[idx] = base_signal[idx] * weights_base[idx] + smooth_signal[idx] * (1.0 - weights_base[idx])
    return filtered
