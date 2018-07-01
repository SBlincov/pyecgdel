"""
Основной класс ЭКГ, состоящий из экземпляров класса отведения.
"""

import numpy as np
from Source.Model.main.ecg_lead.ecg_lead import *
from Source.Model.main.data_details.ecg_data_details import *
from Source.Infrastructure.main.load_ecg_data import *
from Source.Infrastructure.main.save_ecg_data import *

from Source.Model.main.delineation.qrs.delta.delta import qrs_multi_lead_processing
from Source.Model.main.delineation.p.delta.delta import p_multi_lead_processing
from Source.Model.main.delineation.flutter.flutter import *


class InvalidECG(Exception):
    pass


class ECG:

    def __init__(self, data=LOCAL_DB, name=None, record=None, is_log=False):

        self.name = name
        self.record = record
        self.leads = []
        self.is_log = is_log

        if self.is_log:
            print("================================")
            print("Init ECG ...")

        if data is LOCAL_DB:
            load_data_local(self)

        elif isinstance(data, dict):
            for lead_name in data:

                if self.is_log:
                    print("Init " + str(lead_name) + " ...")

                lead = ECGLead(lead_name, data[lead_name], float(ConfigParams['SAMPLING_RATE']))
                self.leads.append(lead)

                if self.is_log:
                    print("Init " + str(lead_name) + " complete")

            if self.is_log:
                print("Init ECG complete")

    def load_local(self, details):
        load_data_local(self, details)

    def save_local(self, details):
        save_data_local(self, details)

    def cwt_filtration(self):
        if self.is_log:
            print("ECG filtration ...")

        for lead_id in range(0, len(self.leads)):
            if self.is_log:
                print("Filtration " + str(self.leads[lead_id].name) + "...")

            self.leads[lead_id].cwt_filtration()

            if self.is_log:
                print("Filtration " + str(self.leads[lead_id].name) + " complete")

        if self.is_log:
            print("ECG filtration complete")
            print("")

    def common_filtration(self):
        if self.is_log:
            print("ECG filtration ...")

        for lead_id in range(0, len(self.leads)):
            if self.is_log:
                print("Filtration " + str(self.leads[lead_id].name) + "...")

            self.leads[lead_id].common_filtration()

            if self.is_log:
                print("Filtration " + str(self.leads[lead_id].name) + " complete")

        print("ECG filtration complete")
        print("")

    def adaptive_filtration(self):
        if self.is_log:
            print("ECG filtration...")

        for lead_id in range(0, len(self.leads)):

            if self.is_log:
                print("Filtration " + str(self.leads[lead_id].name) + "...")

            self.leads[lead_id].adaptive_filtration()

            if self.is_log:
                print("Filtration " + str(self.leads[lead_id].name) + " complete")

        if self.is_log:
            print("ECG filtration complete")
            print("")

    def dwt(self):
        if self.is_log:
            print("ECG DWT ...")

        for lead_id in range(0, len(self.leads)):
            if self.is_log:
                print("dwt " + str(self.leads[lead_id].name) + " ...")

            self.leads[lead_id].dwt()

            if self.is_log:
                print("dwt " + str(self.leads[lead_id].name) + " complete")

        if self.is_log:
            print("ECG DWT complete")
            print("")

    def delineation(self):

        if self.is_log:
            print("ECG delineation ...")

        for lead_id in range(0, len(self.leads)):

            if self.is_log:
                print("QRS delineation " + str(self.leads[lead_id].name) + " ...")

            self.leads[lead_id].qrs_del()

            if self.is_log:
                print("QRS delineation " + str(self.leads[lead_id].name) + " complete")

        if self.is_log:
            print("")

        if len(self.leads) > 3:
            qrs_multi_lead_processing(self.leads)

        flutter_analysis(self.leads)

        for lead_id in range(0, len(self.leads)):
            if self.is_log:
                print("T delineation " + str(self.leads[lead_id].name) + " ...")

            self.leads[lead_id].t_del()

            if self.is_log:
                print("T delineation " + str(self.leads[lead_id].name) + " complete")
        if self.is_log:
            print("")

        for lead_id in range(0, len(self.leads)):
            if self.is_log:
                print("P delineation " + str(self.leads[lead_id].name) + " ...")

            self.leads[lead_id].p_del()

            if self.is_log:
                print("P delineation " + str(self.leads[lead_id].name) + " complete")

        if self.is_log:
            print("")

        if len(self.leads) > 3:
            p_multi_lead_processing(self.leads)

        for lead_id in range(0, len(self.leads)):
            if self.is_log:
                self.leads[lead_id].print_del_info()

        if self.is_log:
            print("ECG delineation complete")
            print("")

    def del_correction(self):
        if self.is_log:
            print("ECG del correction ...")

        for lead_id in range(0, len(self.leads)):
            self.leads[lead_id].del_correction()

        if self.is_log:
            print("ECG del correction complete")
            print("")

    def init_plot_data(self):
        for lead_id in range(0, len(self.leads)):
            self.leads[lead_id].init_plot_data()

    def add_origin_data_to_dict(self, data_dict, cols_names, id_file):

        if not isinstance(data_dict, dict):
            raise InvalidECGData('data_dict must be dict instance')

        if not isinstance(cols_names, list):
            raise InvalidECGData('columns_names must be list instance')

        for lead_id in range(0, len(self.leads)):
            column_name = self.leads[lead_id].name + "_original"
            data_dict[column_name] = [(id_file, self.leads[lead_id].origin.tolist())]
            cols_names.append(column_name)

    def add_filter_data_to_dict(self, data_dict, columns_names, id_file):

        if not isinstance(data_dict, dict):
            raise InvalidECGData('data_dict must be dict instance')

        if not isinstance(columns_names, list):
            raise InvalidECGData('columns_names must be list instance')

        for lead_id in range(0, len(self.leads)):
            column_name = "json_" + self.leads[lead_id].name + "_filtrated"
            data_dict[column_name] = [(id_file, self.leads[lead_id].filter.tolist())]
            columns_names.append(column_name)

    def add_delineation_data_to_dict(self, data_dict, columns_names, id_file):

        flutter_leads_names = FlutterParams['LEADS_NAMES']

        if not isinstance(data_dict, dict):
            raise InvalidECGData('data_dict must be dict instance')

        if not isinstance(columns_names, list):
            raise InvalidECGData('columns_names must be list instance')

        for lead_id in range(0, len(self.leads)):
            column_name = "json_" + self.leads[lead_id].name + "_p_delineation"
            p_dels_data = []
            for delineation in self.leads[lead_id].p_dels:
                p_dels_data.append(np.asarray([int(delineation.onset_index),
                                               int(delineation.peak_index),
                                               int(delineation.offset_index),
                                               int(delineation.specification.value)], dtype=np.int32).tolist())

            if len(p_dels_data) is 0:
                data_dict[column_name] = [(id_file, np.zeros((0, 4), dtype=np.int32).tolist())]
            elif len(p_dels_data) is 1:
                p_dels_data = np.asarray(p_dels_data, dtype=np.int32)
                np.reshape(p_dels_data, (1, 4))
                p_dels_data = p_dels_data.tolist()
                data_dict[column_name] = [(id_file, p_dels_data)]
            else:
                data_dict[column_name] = [(id_file, np.asarray(p_dels_data, dtype=np.int32).tolist())]
            columns_names.append(column_name)

            if self.leads[lead_id].name in flutter_leads_names:

                column_name = "json_" + self.leads[lead_id].name + "_flutter_delineation"
                flutter_dels_data = []
                for delineation in self.leads[lead_id].flutter_dels:
                    flutter_dels_data.append(np.asarray([int(delineation.onset_index),
                                                   int(delineation.peak_index),
                                                   int(delineation.offset_index),
                                                   int(delineation.specification.value)], dtype=np.int32).tolist())

                if len(flutter_dels_data) is 0:
                    data_dict[column_name] = [(id_file, np.zeros((0, 4), dtype=np.int32).tolist())]
                elif len(flutter_dels_data) is 1:
                    flutter_dels_data = np.asarray(flutter_dels_data, dtype=np.int32)
                    np.reshape(flutter_dels_data, (1, 4))
                    flutter_dels_data = flutter_dels_data.tolist()
                    data_dict[column_name] = [(id_file, flutter_dels_data)]
                else:
                    data_dict[column_name] = [(id_file, np.asarray(flutter_dels_data, dtype=np.int32).tolist())]
                columns_names.append(column_name)


            column_name = "json_" + self.leads[lead_id].name + "_qrs_delineation"
            qrs_dels_data = []
            for delineation in self.leads[lead_id].qrs_dels:
                qrs_dels_data.append(np.asarray([int(delineation.onset_index),
                                                 int(delineation.peak_index),
                                                 int(delineation.offset_index),
                                                 int(delineation.specification.value)], dtype=np.int32).tolist())

            if len(qrs_dels_data) is 0:
                data_dict[column_name] = [(id_file, np.zeros((0, 4), dtype=np.int32).tolist())]
            elif len(qrs_dels_data) is 1:
                qrs_dels_data = np.asarray(qrs_dels_data, dtype=np.int32)
                np.reshape(qrs_dels_data, (1, 4))
                qrs_dels_data = qrs_dels_data.tolist()
                data_dict[column_name] = [(id_file, qrs_dels_data)]
            else:
                data_dict[column_name] = [(id_file, np.asarray(qrs_dels_data, dtype=np.int32).tolist())]
            columns_names.append(column_name)

            column_name = "json_" + self.leads[lead_id].name + "_t_delineation"
            t_dels_data = []
            for delineation in self.leads[lead_id].t_dels:
                t_dels_data.append(np.asarray([int(delineation.onset_index),
                                               int(delineation.peak_index),
                                               int(delineation.offset_index),
                                               int(delineation.specification.value)], dtype=np.int32).tolist())

            if len(t_dels_data) is 0:
                data_dict[column_name] = [(id_file, np.zeros((0, 4), dtype=np.int32).tolist())]
            elif len(t_dels_data) is 1:
                t_dels_data = np.asarray(t_dels_data, dtype=np.int32)
                np.reshape(t_dels_data, (1, 4))
                t_dels_data = t_dels_data.tolist()
                data_dict[column_name] = [(id_file, t_dels_data)]
            else:
                data_dict[column_name] = [(id_file, np.asarray(t_dels_data, dtype=np.int32).tolist())]
            columns_names.append(column_name)

    def add_morphology_data_to_dict(self, data_dict, columns_names, id_file):

        if not isinstance(data_dict, dict):
            raise InvalidECGData('data_dict must be dict instance')

        if not isinstance(columns_names, list):
            raise InvalidECGData('columns_names must be list instance')

        for lead_id in range(0, len(self.leads)):

            column_name = "json_" + self.leads[lead_id].name + "_p_morphology"
            p_morphs_data = []
            for morphology in self.leads[lead_id].p_morphs:
                for morphology_point in morphology.points:
                    p_morphs_data.append([int(morphology.del_id),
                                          str(morphology_point.name),
                                          int(morphology_point.index),
                                          float(morphology_point.value),
                                          int(morphology_point.sign),
                                          int(morphology.degree)])

            data_dict[column_name] = [(id_file, p_morphs_data)]
            columns_names.append(column_name)

            column_name = "json_" + self.leads[lead_id].name + "_qrs_morphology"
            qrs_morphs_data = []
            for morphology in self.leads[lead_id].qrs_morphs:
                for morphology_point in morphology.points:
                    qrs_morphs_data.append([int(morphology.del_id),
                                            str(morphology_point.name),
                                            int(morphology_point.index),
                                            float(morphology_point.value),
                                            int(morphology_point.sign),
                                            int(morphology.degree)])

            data_dict[column_name] = [(id_file, qrs_morphs_data)]
            columns_names.append(column_name)

            column_name = "json_" + self.leads[lead_id].name + "_t_morphology"
            t_morphs_data = []
            for morphology in self.leads[lead_id].t_morphs:
                for morphology_point in morphology.points:
                    t_morphs_data.append([int(morphology.del_id),
                                          str(morphology_point.name),
                                          int(morphology_point.index),
                                          float(morphology_point.value),
                                          int(morphology_point.sign),
                                          int(morphology.degree)])

            data_dict[column_name] = [(id_file, t_morphs_data)]
            columns_names.append(column_name)

    def characteristics(self):
        if self.is_log:
            print("ECG calc characteristics...")

        for lead_id in range(0, len(self.leads)):
            if self.is_log:
                print("Calc characteristics " + str(self.leads[lead_id].name) + "...")

            self.leads[lead_id].calc_characteristics()

            if self.is_log:
                print("Calc characteristics " + str(self.leads[lead_id].name) + " complete")

        if self.is_log:
            print("ECG calc characteristics complete")
            print("=======================================================================================================")
            print("")

    def add_characteristics_data_to_dict(self, data_dict, columns_names, id_file):

        if not isinstance(data_dict, dict):
            raise InvalidECGData('data_dict must be dict instance')

        if not isinstance(columns_names, list):
            raise InvalidECGData('columns_names must be list instance')

        for lead_id in range(0, len(self.leads)):

            characteristics = self.leads[lead_id].chars
            characteristics_data_names = []
            characteristics_data_values = []
            for characteristic in characteristics:
                characteristics_data_names.append(characteristic[0].name)
                if characteristic[1] is not 'n':
                    characteristics_data_values.append(characteristic[1])
                else:
                    characteristics_data_values.append(None)
            column_name = "json_" + self.leads[lead_id].name + "_characteristics"
            data_dict[column_name] = [(id_file, [characteristics_data_names, characteristics_data_values])]
            columns_names.append(column_name)


    def add_plot_data_to_dict(self, data_dict, columns_names, id_file):

        if not isinstance(data_dict, dict):
            raise InvalidECGData('data_dict must be dict instance')

        if not isinstance(columns_names, list):
            raise InvalidECGData('columns_names must be list instance')

        for lead_id in range(0, len(self.leads)):

            for plot_data_key in self.leads[lead_id].qrs_plot_data.dict:

                column_name = "json_" + self.leads[lead_id].name + "_" + plot_data_key.name
                data_dict[column_name] = [(id_file, self.leads[lead_id].qrs_plot_data.dict[plot_data_key])]
                columns_names.append(column_name)

