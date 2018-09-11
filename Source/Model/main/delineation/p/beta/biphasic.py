from Source.Model.main.delineation.peaks_zcs_ids import is_prev_zc_exist, is_next_zc_exist
from Source.Model.main.delineation.wave_delineation import WaveSpecification
from Source.Model.main.params.p import PParams

def check_left_biphasic_p(triplet, ecg_lead, zcs, delineation):
    left_peak_zc_id = triplet.left_zc_id
    left_peak_zc = zcs[left_peak_zc_id]

    right_peak_zc_id = triplet.right_zc_id
    right_peak_zc = zcs[right_peak_zc_id]

    rate = ecg_lead.rate

    biphasic_th_more_peak_zc = float(PParams['ALPHA_BIPHASE_AMPL_MORE']) * abs(right_peak_zc.s_r_mm.value)
    biphasic_th_less_peak_zc = float(PParams['ALPHA_BIPHASE_AMPL_LESS']) * abs(right_peak_zc.s_r_mm.value)

    if biphasic_th_more_peak_zc < abs(left_peak_zc.s_l_mm.value) < biphasic_th_less_peak_zc:

        if is_prev_zc_exist(zcs, left_peak_zc_id, float(PParams['ALPHA_PEAK_BEGIN_SHIFT']) * rate):
            prev_zc_id = left_peak_zc_id - 1
            prev_zc = zcs[prev_zc_id]

            biphasic_th_more_prev_zc = float(PParams['ALPHA_BIPHASE_AMPL_MORE']) * abs(prev_zc.s_r_mm.value)
            biphasic_th_less_prev_zc = float(PParams['ALPHA_BIPHASE_AMPL_LESS']) * abs(prev_zc.s_r_mm.value)

            if biphasic_th_more_prev_zc < abs(prev_zc.s_l_mm.value) < biphasic_th_less_prev_zc:
                amplitude = abs(zcs[left_peak_zc_id].s_l_mm.value) + abs(zcs[right_peak_zc_id].s_r_mm.value)

                if prev_zc.s_ampl > float(PParams['ALPHA_BIPHASE_AMPL']) * amplitude:
                    delineation.specification = WaveSpecification.biphasic
                    triplet.left_zc_id = prev_zc_id


def check_right_biphasic_p(triplet, ecg_lead, zcs, delineation):
    left_peak_zc_id = triplet.left_zc_id
    left_peak_zc = zcs[left_peak_zc_id]

    right_peak_zc_id = triplet.right_zc_id
    right_peak_zc = zcs[right_peak_zc_id]

    sampling_rate = ecg_lead.sampling_rate

    biphasic_th_more_peak_zc = float(PParams['ALPHA_BIPHASE_AMPL_MORE']) * abs(right_peak_zc.s_r_mm.value)
    biphasic_th_less_peak_zc = float(PParams['ALPHA_BIPHASE_AMPL_LESS']) * abs(right_peak_zc.s_r_mm.value)

    if biphasic_th_more_peak_zc < abs(left_peak_zc.s_l_mm.value) < biphasic_th_less_peak_zc:

        if is_next_zc_exist(zcs, right_peak_zc_id, float(PParams['ALPHA_PEAK_BEGIN_SHIFT']) * sampling_rate):
            next_zc_id = right_peak_zc_id + 1
            next_zc = zcs[next_zc_id]

            biphasic_th_more_next_zc = float(PParams['ALPHA_BIPHASE_AMPL_MORE']) * abs(next_zc.right_mm.value)
            biphasic_th_less_next_zc = float(PParams['ALPHA_BIPHASE_AMPL_LESS']) * abs(next_zc.right_mm.value)

            if biphasic_th_more_next_zc < abs(next_zc.s_l_mm.value) <= biphasic_th_less_next_zc:

                amplitude = abs(zcs[left_peak_zc_id].s_l_mm.value) + abs(zcs[right_peak_zc_id].s_r_mm.value)

                if next_zc.s_ampl > float(PParams['ALPHA_BIPHASE_AMPL']) * amplitude:
                    delineation.specification = WaveSpecification.biphasic

                    triplet.right_zc_id = next_zc_id
