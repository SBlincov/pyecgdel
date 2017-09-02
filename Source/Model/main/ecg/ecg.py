"""
Основной класс ЭКГ, состоящий из экземпляров класса отведения.
"""

import numpy as np
from Source.Model.main.ecg_lead.ecg_lead import *
from Source.Model.main.data_details.ecg_data_details import *
from Source.Infrastructure.main.load_ecg_data import *
from Source.Infrastructure.main.save_ecg_data import *


class InvalidECG(Exception):
    pass


class ECG:

    def __init__(self, data=LOCAL_DB, name=None, record=None):
        self.name = name
        self.record = record
        self.leads = []
        print("=======================================================================================================")
        if data is LOCAL_DB:
            load_ecg_data_local(self)

        elif isinstance(data, dict):
            print("Init ecg from CardioBase...")
            for lead_name in data:
                print("Init " + str(lead_name) + "...")
                lead = ECGLead(lead_name, data[lead_name], float(ConfigParams['SAMPLING_RATE']))
                self.leads.append(lead)
                print("Init " + str(lead_name) + " complete")

            print("Init ecg from CardioBase...")
            print("")

    def load_data_local(self, details):
        load_ecg_data_local(self, details)

    def save_data_local(self, details):
        save_ecg_data_local(self, details)

    def add_original_data_to_dict(self, data_dict, columns_names, id_file):

        if not isinstance(data_dict, dict):
            raise InvalidECGData('data_dict must be dict instance')

        if not isinstance(columns_names, list):
            raise InvalidECGData('columns_names must be list instance')

        for lead_id in range(0, len(self.leads)):
            column_name = self.leads[lead_id].name + "_original"
            data_dict[column_name] = [(id_file, self.leads[lead_id].original)]
            columns_names.append(column_name)

    def cwt_filtration(self):
        print("ECG filtration...")
        for lead_id in range(0, len(self.leads)):
            print("Filtration " + str(self.leads[lead_id].name) + "...")
            self.leads[lead_id].cwt_filtration()
            print("Filtration " + str(self.leads[lead_id].name) + " complete")
        print("ECG filtration complete")
        print("")

    def add_filtrated_data_to_dict(self, data_dict, columns_names, id_file):

        if not isinstance(data_dict, dict):
            raise InvalidECGData('data_dict must be dict instance')

        if not isinstance(columns_names, list):
            raise InvalidECGData('columns_names must be list instance')

        for lead_id in range(0, len(self.leads)):
            column_name = "json_" + self.leads[lead_id].name + "_filtrated"
            data_dict[column_name] = [(id_file, self.leads[lead_id].filtrated.tolist())]
            columns_names.append(column_name)

    def common_filtration(self):
        for lead_id in range(0, len(self.leads)):
            self.leads[lead_id].common_filtration()

    def dwt(self):
        print("ECG dwt...")
        for lead_id in range(0, len(self.leads)):
            print("dwt " + str(self.leads[lead_id].name) + "...")
            self.leads[lead_id].dwt()
            print("dwt " + str(self.leads[lead_id].name) + " complete")
        print("ECG dwt complete")
        print("")

    def delineation(self):
        print("ECG delineation...")
        for lead_id in range(0, len(self.leads)):
            print("Delineation " + str(self.leads[lead_id].name) + "...")
            self.leads[lead_id].delineation()
            print("Delineation " + str(self.leads[lead_id].name) + " complete")

        # self.all_leads_correction()

        print("ECG delineation complete")

        for lead_id in range(0, len(self.leads)):

            p_dels = self.leads[lead_id].p_dels
            num_p_dels = 0
            for p_dels_seq in p_dels:
                num_p_dels += len(p_dels_seq)

            qrs_dels = self.leads[lead_id].qrs_dels
            num_qrs_dels = 0
            for qrs_dels_seq in qrs_dels:
                num_qrs_dels += len(qrs_dels_seq)

            t_dels = self.leads[lead_id].t_dels
            num_t_dels = 0
            for t_dels_seq in t_dels:
                num_t_dels += len(t_dels_seq)

            print(str(self.leads[lead_id].name) + " num dels: p: " + str(num_p_dels) + " qrs: " + str(num_qrs_dels) + " t: " + str(num_t_dels))

        print("")

    def all_leads_correction(self):

        all_sizes_dels = []
        dict_dels = dict()
        mutability_percentage_p = float(PParams['MUTABILITY_PERCENTAGE'])
        mutability_percentage_qrs = float(QRSParams['MUTABILITY_PERCENTAGE'])
        mutability_percentage_t = float(TParams['MUTABILITY_PERCENTAGE'])
        stability_num_leads_min_part = float(ConfigParams['NUM_LEADS_STABLE_LIMIT'])
        stability_num_leads = int(len(self.leads) * stability_num_leads_min_part)

        max_num_qrs_dels = 0

        for lead_id in range(0, len(self.leads)):

            p_dels = self.leads[lead_id].p_dels
            sizes_p_dels = []
            for p_dels_seq in p_dels:
                sizes_p_dels.append(len(p_dels_seq))

            qrs_dels = self.leads[lead_id].qrs_dels
            sizes_qrs_dels = []
            for qrs_dels_seq in qrs_dels:
                sizes_qrs_dels.append(len(qrs_dels_seq))
                if len(qrs_dels_seq) > max_num_qrs_dels:
                    max_num_qrs_dels = len(qrs_dels_seq)

            t_dels = self.leads[lead_id].t_dels
            sizes_t_dels = []
            for t_dels_seq in t_dels:
                sizes_t_dels.append(len(t_dels_seq))

            all_sizes_dels.append([sizes_p_dels, sizes_qrs_dels, sizes_t_dels])

            tmp_list = [tuple(sizes_p_dels), tuple(sizes_qrs_dels), tuple(sizes_t_dels)]
            tuple_sizes_dels = tuple(tmp_list)
            if tuple_sizes_dels in dict_dels:
                dict_dels[tuple_sizes_dels][0] += 1
                dict_dels[tuple_sizes_dels][1].append(lead_id)
            else:
                dict_dels[tuple_sizes_dels] = []
                dict_dels[tuple_sizes_dels].append(1)
                dict_dels[tuple_sizes_dels].append([lead_id])

        is_ecg_stable = False
        most_frequent_sizes = []
        list_correct_leads_ids = []
        for dict_dels_key in dict_dels:
            if dict_dels[dict_dels_key][0] >= stability_num_leads and max(all_sizes_dels[dict_dels[dict_dels_key][1][0]][1]) > int(0.5 * max_num_qrs_dels):
                is_ecg_stable = True
                most_frequent_sizes = dict_dels_key
                list_correct_leads_ids = dict_dels[dict_dels_key][1]
                stability_num_leads = dict_dels[dict_dels_key][0]

        if is_ecg_stable:
            for lead_id in range(0, len(self.leads)):
                sizes_dels = all_sizes_dels[lead_id]
                sizes_p_dels = sizes_dels[0]
                sizes_qrs_dels = sizes_dels[1]
                sizes_t_dels = sizes_dels[2]

                is_lead_need_to_change = False

                for sizes_p_del_id in range(0, len(sizes_p_dels)):
                    if len(most_frequent_sizes[0]) == len(sizes_p_dels):
                        if abs(sizes_p_dels[sizes_p_del_id] - most_frequent_sizes[0][sizes_p_del_id]) > mutability_percentage_p * most_frequent_sizes[0][sizes_p_del_id]:
                            is_lead_need_to_change = True
                            break
                    else:
                        is_lead_need_to_change = True

                for sizes_qrs_del_id in range(0, len(sizes_qrs_dels)):
                    if len(most_frequent_sizes[1]) == len(sizes_qrs_dels):
                        if abs(sizes_qrs_dels[sizes_qrs_del_id] - most_frequent_sizes[1][sizes_qrs_del_id]) > mutability_percentage_qrs * most_frequent_sizes[1][sizes_qrs_del_id]:
                            is_lead_need_to_change = True
                            break
                    else:
                        is_lead_need_to_change = True

                for sizes_t_del_id in range(0, len(sizes_t_dels)):
                    if len(most_frequent_sizes[2]) == len(sizes_t_dels):
                        if abs(sizes_t_dels[sizes_t_del_id] - most_frequent_sizes[2][sizes_t_del_id]) > mutability_percentage_t * most_frequent_sizes[2][sizes_t_del_id]:
                            is_lead_need_to_change = True
                            break
                    else:
                        is_lead_need_to_change = True

                if is_lead_need_to_change:
                    self.leads[lead_id].p_dels = self.leads[list_correct_leads_ids[0]].p_dels
                    self.leads[lead_id].qrs_dels = self.leads[list_correct_leads_ids[0]].qrs_dels
                    self.leads[lead_id].t_dels = self.leads[list_correct_leads_ids[0]].t_dels

    def add_delineation_data_to_dict(self, data_dict, columns_names, id_file):

        if not isinstance(data_dict, dict):
            raise InvalidECGData('data_dict must be dict instance')

        if not isinstance(columns_names, list):
            raise InvalidECGData('columns_names must be list instance')

        for lead_id in range(0, len(self.leads)):
            column_name = "json_" + self.leads[lead_id].name + "_p_delineation"
            column_name_doc = column_name + "_doc"
            p_dels_data = []
            for del_seq in self.leads[lead_id].p_dels:
                for delineation in del_seq:
                    p_dels_data.append(np.asarray([int(delineation.onset_index),
                                                   int(delineation.peak_index),
                                                   int(delineation.offset_index),
                                                   int(delineation.specification.value)], dtype=np.int32).tolist())

            if len(p_dels_data) is 0:
                data_dict[column_name] = [(id_file, np.zeros((0, 4), dtype=np.int32).tolist())]
                data_dict[column_name_doc] = [(id_file, np.zeros((0, 4), dtype=np.int32).tolist())]
            elif len(p_dels_data) is 1:
                p_dels_data = np.asarray(p_dels_data, dtype=np.int32)
                np.reshape(p_dels_data, (1, 4))
                p_dels_data = p_dels_data.tolist()
                data_dict[column_name] = [(id_file, p_dels_data)]
                data_dict[column_name_doc] = [(id_file, p_dels_data)]
            else:
                data_dict[column_name] = [(id_file, np.asarray(p_dels_data, dtype=np.int32).tolist())]
                data_dict[column_name_doc] = [(id_file, np.asarray(p_dels_data, dtype=np.int32).tolist())]
            columns_names.append(column_name)
            columns_names.append(column_name_doc)

            column_name = "json_" + self.leads[lead_id].name + "_qrs_delineation"
            column_name_doc = column_name + "_doc"
            qrs_dels_data = []
            for del_seq in self.leads[lead_id].qrs_dels:
                for delineation in del_seq:
                    qrs_dels_data.append(np.asarray([int(delineation.onset_index),
                                                     int(delineation.peak_index),
                                                     int(delineation.offset_index),
                                                     int(delineation.specification.value)], dtype=np.int32).tolist())

            if len(qrs_dels_data) is 0:
                data_dict[column_name] = [(id_file, np.zeros((0, 4), dtype=np.int32).tolist())]
                data_dict[column_name_doc] = [(id_file, np.zeros((0, 4), dtype=np.int32).tolist())]
            elif len(qrs_dels_data) is 1:
                qrs_dels_data = np.asarray(qrs_dels_data, dtype=np.int32)
                np.reshape(qrs_dels_data, (1, 4))
                qrs_dels_data = qrs_dels_data.tolist()
                data_dict[column_name] = [(id_file, qrs_dels_data)]
                data_dict[column_name_doc] = [(id_file, qrs_dels_data)]
            else:
                data_dict[column_name] = [(id_file, np.asarray(qrs_dels_data, dtype=np.int32).tolist())]
                data_dict[column_name_doc] = [(id_file, np.asarray(qrs_dels_data, dtype=np.int32).tolist())]
            columns_names.append(column_name)
            columns_names.append(column_name_doc)

            column_name = "json_" + self.leads[lead_id].name + "_t_delineation"
            column_name_doc = column_name + "_doc"
            t_dels_data = []
            for del_seq in self.leads[lead_id].t_dels:
                for delineation in del_seq:
                    t_dels_data.append(np.asarray([int(delineation.onset_index),
                                                   int(delineation.peak_index),
                                                   int(delineation.offset_index),
                                                   int(delineation.specification.value)], dtype=np.int32).tolist())

            if len(t_dels_data) is 0:
                data_dict[column_name] = [(id_file, np.zeros((0, 4), dtype=np.int32).tolist())]
                data_dict[column_name_doc] = [(id_file, np.zeros((0, 4), dtype=np.int32).tolist())]
            elif len(t_dels_data) is 1:
                t_dels_data = np.asarray(t_dels_data, dtype=np.int32)
                np.reshape(t_dels_data, (1, 4))
                t_dels_data = t_dels_data.tolist()
                data_dict[column_name] = [(id_file, t_dels_data)]
                data_dict[column_name_doc] = [(id_file, t_dels_data)]
            else:
                data_dict[column_name] = [(id_file, np.asarray(t_dels_data, dtype=np.int32).tolist())]
                data_dict[column_name_doc] = [(id_file, np.asarray(t_dels_data, dtype=np.int32).tolist())]
            columns_names.append(column_name)
            columns_names.append(column_name_doc)

    def add_morphology_data_to_dict(self, data_dict, columns_names, id_file):

        if not isinstance(data_dict, dict):
            raise InvalidECGData('data_dict must be dict instance')

        if not isinstance(columns_names, list):
            raise InvalidECGData('columns_names must be list instance')

        for lead_id in range(0, len(self.leads)):

            column_name = "json_" + self.leads[lead_id].name + "_qrs_delineation"
            column_name_doc = column_name + "_doc"
            qrs_morphs_data = []
            for morph_seq in self.leads[lead_id].qrs_morphs:
                for morphology in morph_seq:
                    for morphology_point in morphology.points:
                        qrs_morphs_data.append([int(morphology.del_id),
                                                str(morphology_point.name),
                                                int(morphology_point.index),
                                                float(morphology_point.value),
                                                int(morphology_point.sign)])

            data_dict[column_name] = [(id_file, qrs_morphs_data)]
            data_dict[column_name_doc] = [(id_file, qrs_morphs_data)]
            columns_names.append(column_name)
            columns_names.append(column_name_doc)

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

            characteristics = self.leads[lead_id].characteristics
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

