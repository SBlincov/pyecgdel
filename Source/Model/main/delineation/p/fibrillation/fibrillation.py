from Source.Model.main.params.p_default import *
from Source.Model.main.ecg_lead.ecg_lead import *
from Source.Model.main.modulus_maxima.routines import *
from Source.Model.main.delineation.p.delineation import *
from Source.Model.main.delineation.p.zcs import *


def fib_analysis_imbalance(ecg_lead):

    signal = ecg_lead.filter

    p_dels = ecg_lead.p_dels
    p_morphs = ecg_lead.p_morphs

    for del_id in range(len(p_dels)-1, -1, -1):

        # Check for length imbalance

        is_del_len = False
        left_len = float(p_dels[del_id].onset_index - p_dels[del_id].peak_index)
        right_len = float(p_dels[del_id].peak_index - p_dels[del_id].offset_index)
        len_part = float(PParams['FIB_LEN_PART'])

        if left_len / right_len > len_part or left_len / right_len < 1.0 / len_part:
            is_del_len = True

        # Check for amplitude imbalance

        is_del_ampl = False
        left_ampl = abs(signal[p_dels[del_id].onset_index] - signal[p_dels[del_id].peak_index])
        right_ampl = abs(signal[p_dels[del_id].peak_index] - signal[p_dels[del_id].offset_index])
        ampl_part = float(PParams['FIB_AMPL_PART'])

        if left_ampl / right_ampl > ampl_part or left_ampl / right_ampl < 1.0 / ampl_part:
            is_del_ampl = True

        if is_del_len or is_del_ampl:
            p_dels.pop(del_id)
            p_morphs.pop(del_id)


def fib_analysis_shortage(ecg_lead):

    target = len(ecg_lead.qrs_dels) - 1
    num_p_dels = len(ecg_lead.p_dels)

    part = float(PParams['FIB_DELS_PART'])
    min_num_dels = int(target * part)

    if num_p_dels < min_num_dels:
        ecg_lead.p_dels = []
        ecg_lead.p_morphs = []


