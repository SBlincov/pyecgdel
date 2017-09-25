"""
Класс отведения сигнала ЭКГ
"""

from Source.Model.main.delineation.qrs.delineation import *
from Source.Model.main.filtration.cwt_filtration import *
from Source.Model.main.filtration.common_filtration import *
from Source.Model.main.delineation.p.delineation import *
from Source.Model.main.discrete_wavelet_transform.wdc import *
from Source.Model.main.data_details.ecg_data_details import *
from Source.Model.main.delineation.t.delineation import *
from Source.Model.main.characteristics.qrs_characteristics import *
from Source.Model.main.characteristics.p_characteristics import *
from Source.Model.main.characteristics.t_characteristics import *


class InvalidECGLead(Exception):
    pass


class ECGLead:

    def __init__(self, name, signal, sampling_rate):

        signal = np.asarray(signal)

        if signal is np.empty:
            raise InvalidECGLead('Error! Empty ecg lead signal')

        if sampling_rate < 0.0:
            raise InvalidECGLead('Error! Negative sampling rate')

        self.name = name
        self.original = signal
        self.filtrated = signal
        self.sampling_rate = sampling_rate
        self.wdc = []

        self.cur_qrs_dels_seq = []
        self.cur_qrs_morph_seq = []

        self.cur_t_dels_seq = []
        self.cur_t_morph_seq = []

        self.cur_p_dels_seq = []

        self.qrs_dels = []
        self.qrs_morphs = []

        self.t_dels = []
        self.t_morphs = []

        self.p_dels = []

        self.characteristics = []

    def cwt_filtration(self):
        self.filtrated = cwt_filtration(self.original)

    def common_filtration(self):
        self.filtrated = common_filtration(self)

    def dwt(self):
        self.wdc = get_wdc(self.filtrated)

    def delineation(self):
        cur_qrs_dels_seq, cur_qrs_morph_seq = get_qrs_delineations(self, 0, len(self.wdc[0]))
        self.cur_qrs_dels_seq = cur_qrs_dels_seq
        self.cur_qrs_morph_seq = cur_qrs_morph_seq

        cur_t_dels_seq, cur_t_morph_seq = get_t_delineations(self)
        self.cur_t_dels_seq = cur_t_dels_seq
        self.cur_t_morph_seq = cur_t_morph_seq

        self.cur_p_dels_seq = get_p_delineations(self)

        self.qrs_dels.append(self.cur_qrs_dels_seq)
        self.qrs_morphs.append(self.cur_qrs_morph_seq)

        self.t_dels.append(self.cur_t_dels_seq)
        self.t_morphs.append(self.cur_t_morph_seq)

        self.p_dels.append(self.cur_p_dels_seq)

        if not self.cur_qrs_dels_seq:
            return

        next_seq_start = self.cur_qrs_dels_seq[-1].offset_index

        self.cur_qrs_dels_seq = []
        self.cur_qrs_morph_seq = []

        self.cur_t_dels_seq = []
        self.cur_t_morph_seq = []

        self.cur_p_dels_seq = []

        while next_seq_start < int(len(self.wdc[0]) * 0.8):

            cur_qrs_dels_seq, cur_qrs_morph_seq = get_qrs_delineations(self, next_seq_start, len(self.wdc[0]))
            self.cur_qrs_dels_seq = cur_qrs_dels_seq
            self.cur_qrs_morph_seq = cur_qrs_morph_seq

            cur_t_dels_seq, cur_t_morph_seq = get_t_delineations(self)
            self.cur_t_dels_seq = cur_t_dels_seq
            self.cur_t_morph_seq = cur_t_morph_seq

            self.cur_p_dels_seq = get_p_delineations(self)

            if self.cur_qrs_dels_seq:
                self.qrs_dels.append(self.cur_qrs_dels_seq)
                self.qrs_morphs.append(self.cur_qrs_morph_seq)

                self.t_dels.append(self.cur_t_dels_seq)
                self.t_morphs.append(self.cur_t_morph_seq)

                self.p_dels.append(self.cur_p_dels_seq)

                next_seq_start = self.cur_qrs_dels_seq[-1].offset_index
            else:
                next_seq_start += int((len(self.wdc[0]) - next_seq_start) * 0.1)

            self.cur_qrs_dels_seq = []
            self.cur_qrs_morph_seq = []

            self.cur_t_dels_seq = []
            self.cur_t_morph_seq = []

            self.cur_p_dels_seq = []

    def calc_characteristics(self):
        qrs_characteristics = get_qrs_characteristics(self)
        p_characteristics = get_p_characteristics(self)
        t_characteristics = get_t_characteristics(self)
        self.characteristics = qrs_characteristics + p_characteristics + t_characteristics

