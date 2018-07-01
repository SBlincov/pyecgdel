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

        self.leads = []
        self.name = name
        self.record = record

        self._is_dwt = False
        self._is_delineation = False
        self._is_adaptive_filtration = False
        self._is_characteristics = False
        self._is_init_plot_data = False

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

    def _load_local(self, details):
        load_data_local(self, details)

    def _save_local(self, details):
        save_data_local(self, details)

    def _cwt_filtration(self):
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

    def _common_filtration(self):
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

    def _adaptive_filtration(self):

        if self._is_adaptive_filtration:
            return

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

        self._is_adaptive_filtration = True

    def _dwt(self):
        if self._is_dwt:
            return

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

        self._is_dwt = True

    def _delineation(self):

        if self._is_delineation:
            return

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

        self._is_delineation = True

    def _del_correction(self):
        if self.is_log:
            print("ECG del correction ...")

        for lead_id in range(0, len(self.leads)):
            self.leads[lead_id].del_correction()

        if self.is_log:
            print("ECG del correction complete")
            print("")

    def _characteristics(self):
        if self._is_characteristics:
            return

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
            print(
                "=======================================================================================================")
            print("")

        self._is_characteristics = True

    def _init_plot_data(self):

        if self._is_init_plot_data:
            return

        self._characteristics()

        for lead_id in range(0, len(self.leads)):
            self.leads[lead_id].init_plot_data()

        self._is_init_plot_data = True

    def _add_origin_data_to_dict(self, data_dict, cols_names, id_file):

        if not isinstance(data_dict, dict):
            raise InvalidECGData('data_dict must be dict instance')

        if not isinstance(cols_names, list):
            raise InvalidECGData('columns_names must be list instance')

        for lead_id in range(0, len(self.leads)):
            column_name = self.leads[lead_id].name + "_original"
            data_dict[column_name] = [(id_file, self.leads[lead_id].origin.tolist())]
            cols_names.append(column_name)

    def _add_filter_data_to_dict(self, data_dict, columns_names, id_file):

        if not isinstance(data_dict, dict):
            raise InvalidECGData('data_dict must be dict instance')

        if not isinstance(columns_names, list):
            raise InvalidECGData('columns_names must be list instance')

        for lead_id in range(0, len(self.leads)):
            column_name = "json_" + self.leads[lead_id].name + "_filtrated"
            data_dict[column_name] = [(id_file, self.leads[lead_id].filter.tolist())]
            columns_names.append(column_name)

    def _add_delineation_data_to_dict(self, data_dict, columns_names, id_file):

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

    def _add_morphology_data_to_dict(self, data_dict, columns_names, id_file):

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

    def _add_characteristics_data_to_dict(self, data_dict, columns_names, id_file):

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

    def _add_plot_data_to_dict(self, data_dict, columns_names, id_file):

        if not isinstance(data_dict, dict):
            raise InvalidECGData('data_dict must be dict instance')

        if not isinstance(columns_names, list):
            raise InvalidECGData('columns_names must be list instance')

        for lead_id in range(0, len(self.leads)):

            for plot_data_key in self.leads[lead_id].qrs_plot_data.dict:

                column_name = "json_" + self.leads[lead_id].name + "_" + plot_data_key.name
                data_dict[column_name] = [(id_file, self.leads[lead_id].qrs_plot_data.dict[plot_data_key])]
                columns_names.append(column_name)

    def get_filtrated(self):
        self._adaptive_filtration()
        return {lead.name:lead.filter for lead in self.leads}

    def _two_dimensions_delineation(self, array):
        if len(array) is 0:
            return np.zeros((0, 4), dtype=np.int32).tolist()
        elif len(array) is 1:
            result = np.asarray(array, dtype=np.int32)
            np.reshape(result, (1, 4))
            return result.tolist()
        else:
            return np.asarray(array, dtype=np.int32).tolist()

    def _create_array_from_delineation(self, dels):
        result = []
        for delineation in dels:
            result.append(np.asarray(
                [int(delineation.onset_index),
                 int(delineation.peak_index),
                 int(delineation.offset_index),
                 int(delineation.specification.value)], dtype=np.int32).tolist())
        return self._two_dimensions_delineation(result)

    def get_delineation(self):
        self._delineation()
        data_dict = dict()
        flutter_leads_names = FlutterParams['LEADS_NAMES']

        for lead in self.leads:
            lead_name = lead.name
            data_dict[lead_name] = dict()
            data_dict[lead_name]["p"] = self._create_array_from_delineation(lead.p_dels)
            data_dict[lead_name]["qrs"] = self._create_array_from_delineation(lead.qrs_dels)
            data_dict[lead_name]["t"] = self._create_array_from_delineation(lead.t_dels)
            if lead_name in flutter_leads_names:
                data_dict[lead_name]["flutter"] = self._create_array_from_delineation(lead.flutter_dels)

        return data_dict

    def _create_array_from_morphology(self, morphs):
        result = []
        for morphology in morphs:
            for morphology_point in morphology.points:
                result.append([
                    int(morphology.del_id),
                    str(morphology_point.name),
                    int(morphology_point.index),
                    float(morphology_point.value),
                    int(morphology_point.sign),
                    int(morphology.degree)])
        return result

    def get_morphology(self):
        self._delineation()
        data_dict = dict()
        for lead in self.leads:
            lead_name = lead.name
            data_dict[lead_name] = dict()
            data_dict[lead_name]["p"] = self._create_array_from_morphology(lead.p_morphs)
            data_dict[lead_name]["qrs"] = self._create_array_from_morphology(lead.qrs_morphs)
            data_dict[lead_name]["t"] = self._create_array_from_morphology(lead.t_morphs)
        return data_dict

    def get_characteristics(self):
        self._characteristics()
        data_dict = dict()
        for lead in self.leads:
            characteristics_data_names = []
            characteristics_data_values = []
            for characteristic in lead.chars:
                characteristics_data_names.append(characteristic[0].name)
                if characteristic[1] != 'n':
                    characteristics_data_values.append(characteristic[1])
                else:
                    characteristics_data_values.append(None)
            data_dict[lead.name] = dict(zip(characteristics_data_names, characteristics_data_values))
        return data_dict

    def get_plot_data(self):
        self._init_plot_data()
        data_dict = dict()
        for lead in self.leads:
            for plot_data_key in lead.qrs_plot_data.dict:
                data_dict[lead.name] = lead.qrs_plot_data.dict[plot_data_key]
        return data_dict

