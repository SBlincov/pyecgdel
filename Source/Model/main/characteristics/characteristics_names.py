"""
Перечисление основных характеристик сигнала ЭКГ, которые используются в дальнейших подмодулях.
"""

from enum import Enum


class CharacteristicsNames(Enum):

    # Regular
    mean_NN = "mean_NN"
    max_sub_min_NN = "max_sub_min_NN"

    # Statistical
    SDNN = "SDNN"
    SDANN = "SDANN"
    SDNNindex = "SDNNindex"
    RMSSD = "RMSSD"
    NN50 = "NN50"
    pNN50 = "pNN50"

    # Geometry
    triangular_index = "triangular index"
    TINN = "TINN"

    mean_rr = "mean_rr"
    std_rr = "std_rr"
    mean_qrs = "mean_qrs"
    std_qrs = "std_qrs"
    normal_qrs = "normal_qrs"
    flexure_qrs = "flexure_qrs"
    extra_qrs = "extra_qrs"
    mean_r_val = "mean_r_val"
    std_r_val = "std_r_val"
    max_r_val = "max_r_val"
    min_r_val = "min_r_val"

    presence_p = "presence_p"
    mean_p = "mean_p"
    std_p = "std_p"
    mean_pq = "mean_pq"
    std_pq = "std_pq"
    normal_p = "normal_p"
    flexure_p = "flexure_p"
    biphasic_p = "biphasic_p"
    atrial_fibrillation_p = "atrial_fibrillation_p"
    mean_p_val = "mean_p_val"
    std_p_val = "std_p_val"
    max_p_val = "max_p_val"
    min_p_val = "min_p_val"

    presence_t = "presence_t"
    mean_t = "mean_t"
    std_t = "std_t"
    mean_qt = "mean_qt"
    std_qt = "std_qt"
    mean_st = "mean_st"
    std_st = "std_st"
    normal_t = "normal_t"
    flexure_t = "flexure_t"
    biphasic_t = "biphasic_t"
    mean_t_val = "mean_t_val"
    std_t_val = "std_t_val"
    max_t_val = "max_t_val"
    min_t_val = "min_t_val"


