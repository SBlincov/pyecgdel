"""
Класс отведения сигнала ЭКГ
"""

from Source.Model.main.delineation.qrs.delineation import *
from Source.Model.main.filtration.cwt_filtration import *
from Source.Model.main.filtration.common_filtration import *
from Source.Model.main.filtration.adaptive_filtration import *
from Source.Model.main.delineation.p.delineation import *
from Source.Model.main.discrete_wavelet_transform.wdc import *
from Source.Model.main.data_details.ecg_data_details import *
from Source.Model.main.delineation.t.delineation import *
from Source.Model.main.characteristics.qrs_characteristics import *
from Source.Model.main.characteristics.p_characteristics import *
from Source.Model.main.characteristics.t_characteristics import *
from Source.Model.main.plot_data.qrs import QRSPlotData


class InvalidECGLead(Exception):
    pass


class ECGLead:

    def __init__(self, name, signal, rate):

        signal = np.asarray(signal)

        if signal is np.empty:
            raise InvalidECGLead('Error! Empty ecg lead signal')

        if rate < 0.0:
            raise InvalidECGLead('Error! Negative sampling rate')

        self.name = name
        self.origin = signal
        self.filter = signal
        self.rate = rate
        self.wdc = []

        self.qrs_dels = []
        self.qrs_morphs = []

        self.t_dels = []
        self.t_morphs = []

        self.p_dels = []
        self.p_morphs = []

        self.chars = []

        self.qrs_plot_data = []

    def cwt_filtration(self):
        self.filter = cwt_filtration(self.origin)

    def common_filtration(self):
        self.filter = common_filtration(self)

    def adaptive_filtration(self):
        self.filter = adaptive_filtration(self)

    def dwt(self):
        self.wdc = get_wdc(self.filter)

    def qrs_del(self):
        cur_qrs_dels, cur_qrs_morph = get_qrs_dels(self, 0, len(self.wdc[0]))
        self.qrs_dels = cur_qrs_dels
        self.qrs_morphs = cur_qrs_morph

        if cur_qrs_dels:

            next_start = cur_qrs_dels[-1].offset_index

            while next_start < int(len(self.wdc[0]) * float(QRSParams['ALPHA_HUGE_PART'])):

                cur_qrs_dels, cur_qrs_morph = get_qrs_dels(self, next_start, len(self.wdc[0]))
                if cur_qrs_dels:
                    self.qrs_dels += cur_qrs_dels
                    self.qrs_morphs += cur_qrs_morph

                    next_start = cur_qrs_dels[-1].offset_index
                else:
                    next_start += int((len(self.wdc[0]) - next_start) * float(QRSParams['ALPHA_INC']))

    def t_del(self):
        cur_t_dels, cur_t_morph = get_t_dels(self)
        self.t_dels = cur_t_dels
        self.t_morphs = cur_t_morph

    def p_del(self):
        cur_p_dels_seq, cur_p_morph_seq = get_p_dels(self)
        self.p_dels = cur_p_dels_seq
        self.p_morphs = cur_p_morph_seq

    def del_correction(self):
        filter = self.filter

        qrs_morphs = self.qrs_morphs
        for qrs_morph in qrs_morphs:
            for point in qrs_morph.points:
                point.value = filter[point.index]

        t_morphs = self.t_morphs
        for t_morph in t_morphs:
            for point in t_morph.points:
                point.value = filter[point.index]

        p_morphs = self.p_morphs
        for p_morph in p_morphs:
            for point in p_morph.points:
                point.value = filter[point.index]

    def calc_characteristics(self):
        qrs_chars = get_qrs_chars(self)
        p_chars = get_p_chars(self)
        t_chars = get_t_chars(self)
        self.chars = qrs_chars + p_chars + t_chars

    def init_plot_data(self):
        self.qrs_plot_data = QRSPlotData(self)


    def print_del_info(self):

        num_qrs_dels = len(self.qrs_dels)
        num_t_dels = len(self.t_dels)
        num_p_dels = len(self.p_dels)

        print(str(self.name) + ": \t QRS: " + str(num_qrs_dels) + " T: " + str(num_t_dels) + " P: " + str(num_p_dels))


