"""
Вспомогательная структура для распознавания различных морфологий комплексов.
"""

from Source.Model.main.delineation.p.peak import get_p_flexure_zc_id
from Source.Model.main.delineation.wave_delineation import WaveSpecification
from Source.Model.main.params.p import PParams
from Source.Model.main.params.t import TParams


class PeakZCsIds:

    def __init__(self, left_zc_id, center_zc_id, right_zc_id):
        self.left_zc_id = left_zc_id
        self.center_zc_id = center_zc_id
        self.right_zc_id = right_zc_id

    def check_flexure_p(self, ecg_lead, qrs_id, zcs, delineation):

        zc_flexure_id = get_p_flexure_zc_id(ecg_lead, qrs_id, zcs, self.center_zc_id)

        if zc_flexure_id is not -1:
            peak_zc_id = zc_flexure_id
            left_peak_zc_id = zc_flexure_id - 1
            right_peak_zc_id = zc_flexure_id + 1

            self.left_zc_id = left_peak_zc_id
            self.center_zc_id = peak_zc_id
            self.right_zc_id = right_peak_zc_id

            delineation.specification = WaveSpecification.flexure
            delineation.peak_index = zcs[peak_zc_id].index
            # delineation.special_points_indexes.append(zcs[left_peak_zc_id].index)
            # delineation.special_points_indexes.append(zcs[right_peak_zc_id].index)

    def check_left_biphasic_p(self, ecg_lead, zcs, delineation):

        left_peak_zc_id = self.left_zc_id
        left_peak_zc = zcs[left_peak_zc_id]

        right_peak_zc_id = self.right_zc_id
        right_peak_zc = zcs[right_peak_zc_id]

        rate = ecg_lead.rate

        biphasic_th_more_peak_zc = float(PParams['BIPHASIC_AMPLITUDE_MORE']) * abs(right_peak_zc.right_mm.value)
        biphasic_th_less_peak_zc = float(PParams['BIPHASIC_AMPLITUDE_LESS']) * abs(right_peak_zc.right_mm.value)

        if biphasic_th_more_peak_zc < abs(left_peak_zc.left_mm.value) < biphasic_th_less_peak_zc:

            if is_prev_zc_exist(zcs, left_peak_zc_id, float(PParams['ZCS_PEAK_SEARCHING_SHIFT']) * rate):
                prev_zc_id = left_peak_zc_id - 1
                prev_zc = zcs[prev_zc_id]

                biphasic_th_more_prev_zc = float(PParams['BIPHASIC_AMPLITUDE_MORE']) * abs(prev_zc.right_mm.value)
                biphasic_th_less_prev_zc = float(PParams['BIPHASIC_AMPLITUDE_LESS']) * abs(prev_zc.right_mm.value)

                if biphasic_th_more_prev_zc < abs(prev_zc.left_mm.value) < biphasic_th_less_prev_zc:

                    amplitude = abs(zcs[left_peak_zc_id].left_mm.value) + abs(zcs[right_peak_zc_id].right_mm.value)

                    if prev_zc.mm_amplitude > float(PParams['BIPHASIC_AMPLITUDE']) * amplitude:

                        delineation.specification = WaveSpecification.biphasic
                        # delineation.special_points_indexes.append(prev_zc.index)

                        self.left_zc_id = prev_zc_id

    def check_left_biphasic_t(self, ecg_lead, qrs_id, zcs, delineation):

        left_peak_zc_id = self.left_zc_id
        left_peak_zc = zcs[left_peak_zc_id]

        right_peak_zc_id = self.right_zc_id
        right_peak_zc = zcs[right_peak_zc_id]

        cur_qrs_dels_seq = ecg_lead.cur_qrs_dels_seq
        rr = cur_qrs_dels_seq[qrs_id].peak_index - cur_qrs_dels_seq[qrs_id - 1].peak_index

        if is_prev_zc_exist(zcs, left_peak_zc_id, rr):

            prev_zc_id = left_peak_zc_id - 1
            prev_zc = zcs[prev_zc_id]

            amplitude = abs(left_peak_zc.left_mm.value) + abs(right_peak_zc.right_mm.value)

            if prev_zc.mm_amplitude > amplitude * float(TParams['BIPHASIC_AMPLITUDE_LEFT']) \
                    and distance_between_zcs(zcs, prev_zc_id, left_peak_zc_id) < rr * float(TParams['BIPHASIC_LIMIT_SHIFT']):

                delineation.specification = WaveSpecification.biphasic
                # delineation.special_points_indexes.append(prev_zc.index)

                self.left_zc_id = prev_zc_id

    def check_right_biphasic_p(self, ecg_lead, zcs, delineation):

        left_peak_zc_id = self.left_zc_id
        left_peak_zc = zcs[left_peak_zc_id]

        right_peak_zc_id = self.right_zc_id
        right_peak_zc = zcs[right_peak_zc_id]

        sampling_rate = ecg_lead.sampling_rate

        biphasic_th_more_peak_zc = float(PParams['BIPHASIC_AMPLITUDE_MORE']) * abs(right_peak_zc.right_mm.value)
        biphasic_th_less_peak_zc = float(PParams['BIPHASIC_AMPLITUDE_LESS']) * abs(right_peak_zc.right_mm.value)

        if biphasic_th_more_peak_zc < abs(left_peak_zc.left_mm.value) < biphasic_th_less_peak_zc:

            if is_next_zc_exist(zcs, right_peak_zc_id, float(PParams['ZCS_PEAK_SEARCHING_SHIFT']) * sampling_rate):
                next_zc_id = right_peak_zc_id + 1
                next_zc = zcs[next_zc_id]

                biphasic_th_more_next_zc = float(PParams['BIPHASIC_AMPLITUDE_MORE']) * abs(next_zc.right_mm.value)
                biphasic_th_less_next_zc = float(PParams['BIPHASIC_AMPLITUDE_LESS']) * abs(next_zc.right_mm.value)

                if biphasic_th_more_next_zc < abs(next_zc.left_mm.value) <= biphasic_th_less_next_zc:

                    amplitude = abs(zcs[left_peak_zc_id].left_mm.value) + abs(zcs[right_peak_zc_id].right_mm.value)

                    if next_zc.mm_amplitude > float(PParams['BIPHASIC_AMPLITUDE']) * amplitude:

                        delineation.specification = WaveSpecification.biphasic
                        # delineation.special_points_indexes.append(next_zc.index)

                        self.right_zc_id = next_zc_id

    def check_right_biphasic_t(self, ecg_lead, qrs_id, zcs, delineation):

        left_peak_zc_id = self.left_zc_id
        left_peak_zc = zcs[left_peak_zc_id]

        right_peak_zc_id = self.right_zc_id
        right_peak_zc = zcs[right_peak_zc_id]

        cur_qrs_dels_seq = ecg_lead.cur_qrs_dels_seq
        rr = cur_qrs_dels_seq[qrs_id].peak_index - cur_qrs_dels_seq[qrs_id - 1].peak_index

        if is_next_zc_exist(zcs, right_peak_zc_id, rr):

            next_zc_id = right_peak_zc_id + 1
            next_zc = zcs[next_zc_id]

            amplitude = abs(left_peak_zc.left_mm.value) + abs(right_peak_zc.right_mm.value)

            if next_zc.mm_amplitude > amplitude * float(TParams['BIPHASIC_AMPLITUDE_RIGHT']) \
                    and distance_between_zcs(zcs, right_peak_zc_id, next_zc_id) < rr * float(TParams['BIPHASIC_LIMIT_SHIFT']):

                delineation.specification = WaveSpecification.biphasic
                # delineation.special_points_indexes.append(next_zc.index)

                self.right_zc_id = next_zc_id


def is_prev_zc_exist(zcs, zc_id, window):

    result = False

    if zc_id > 0:
        if (zcs[zc_id].index - zcs[zc_id - 1].index) < window:
            result = True

    return result


def is_next_zc_exist(zcs, zc_id, window):

    result = False

    if zc_id < len(zcs) - 1:
        if (zcs[zc_id + 1].index - zcs[zc_id].index) < window:
            result = True

    return result


def distance_between_zcs(zcs, zc_id_left, zc_id_right):
    return zcs[zc_id_right].index - zcs[zc_id_left].index
