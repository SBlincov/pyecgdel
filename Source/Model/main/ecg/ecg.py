"""
Основной класс ЭКГ, состоящий из экземпляров класса отведения.
"""

import numpy as np
from Source.Model.main.ecg_lead.ecg_lead import *
from Source.Model.main.data_details.ecg_data_details import *
from Source.Infrastructure.main.load_ecg_data import *
from Source.Infrastructure.main.save_ecg_data import *

from Source.Model.main.delineation.qrs.delta.delta import multi_lead_processing


class InvalidECG(Exception):
    pass


class ECG:

    def __init__(self, data=LOCAL_DB, name=None, record=None):

        self.name = name
        self.record = record
        self.leads = []

        print("================================")
        print("Init ECG ...")

        if data is LOCAL_DB:
            load_data_local(self)

        elif isinstance(data, dict):
            for lead_name in data:
                print("Init " + str(lead_name) + " ...")
                lead = ECGLead(lead_name, data[lead_name], float(ConfigParams['SAMPLING_RATE']))
                self.leads.append(lead)
                print("Init " + str(lead_name) + " complete")

            print("Init ECG complete")

    def load_local(self, details):
        load_data_local(self, details)

    def save_local(self, details):
        save_data_local(self, details)

    def cwt_filtration(self):
        print("ECG filtration ...")

        for lead_id in range(0, len(self.leads)):
            print("Filtration " + str(self.leads[lead_id].name) + "...")
            self.leads[lead_id].cwt_filtration()
            print("Filtration " + str(self.leads[lead_id].name) + " complete")

        print("ECG filtration complete")
        print("")

    def common_filtration(self):
        print("ECG filtration ...")

        for lead_id in range(0, len(self.leads)):
            print("Filtration " + str(self.leads[lead_id].name) + "...")
            self.leads[lead_id].common_filtration()
            print("Filtration " + str(self.leads[lead_id].name) + " complete")

        print("ECG filtration complete")
        print("")

    def adaptive_filtration(self):
        print("ECG filtration...")
        for lead_id in range(0, len(self.leads)):
            print("Filtration " + str(self.leads[lead_id].name) + "...")
            self.leads[lead_id].adaptive_filtration()
            print("Filtration " + str(self.leads[lead_id].name) + " complete")
        print("ECG filtration complete")
        print("")

    def dwt(self):
        print("ECG DWT ...")

        for lead_id in range(0, len(self.leads)):
            print("dwt " + str(self.leads[lead_id].name) + " ...")
            self.leads[lead_id].dwt()
            print("dwt " + str(self.leads[lead_id].name) + " complete")

        print("ECG DWT complete")
        print("")

    def delineation(self):
        print("ECG delineation ...")

        for lead_id in range(0, len(self.leads)):
            print("QRS delineation " + str(self.leads[lead_id].name) + " ...")
            self.leads[lead_id].qrs_del()
            print("QRS delineation " + str(self.leads[lead_id].name) + " complete")
        print("")

        if len(self.leads) > 1:
            multi_lead_processing(self.leads)

        for lead_id in range(0, len(self.leads)):
            print("T delineation " + str(self.leads[lead_id].name) + " ...")
            self.leads[lead_id].t_del()
            print("T delineation " + str(self.leads[lead_id].name) + " complete")
        print("")

        for lead_id in range(0, len(self.leads)):
            print("P delineation " + str(self.leads[lead_id].name) + " ...")
            self.leads[lead_id].p_del()
            print("P delineation " + str(self.leads[lead_id].name) + " complete")
        print("")

        for lead_id in range(0, len(self.leads)):
            self.leads[lead_id].print_del_info()

        print("ECG delineation complete")
        print("")

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
                                          int(morphology_point.sign)])

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
                                            int(morphology_point.sign)])

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
                                          int(morphology_point.sign)])

            data_dict[column_name] = [(id_file, t_morphs_data)]
            columns_names.append(column_name)

    def characteristics(self):
        print("ECG calc characteristics...")
        for lead_id in range(0, len(self.leads)):
            print("Calc characteristics " + str(self.leads[lead_id].name) + "...")
            self.leads[lead_id].calc_characteristics()
            print("Calc characteristics " + str(self.leads[lead_id].name) + " complete")
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

