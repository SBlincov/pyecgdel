from Source.CardioBase.cardiobase import Cardiobase
from Source.Model.main.ecg.ecg import *

DBConfig.name = 'UNNCyberHeartDatabase'
DBConfig.root = 'pyecgdel'
DBConfig.data_catalogue = 'Data'

DBConfig.config_params = 'properties.txt'
DBConfig.p_params = 'p_params.txt'
DBConfig.qrs_params = 'qrs_params.txt'
DBConfig.t_params = 't_params.txt'
DBConfig.filter_params = 'filter_params.txt'
DBConfig.flutter_params = 'flutter_params.txt'

init_params(params_type=ParamsType.config_params)
init_params(params_type=ParamsType.p_params)
init_params(params_type=ParamsType.qrs_params)
init_params(params_type=ParamsType.t_params)
init_params(params_type=ParamsType.filter_params)
init_params(params_type=ParamsType.flutter_params)

db_path = DBConfig.get_db_path()

cb = Cardiobase()
cb.connect()

max_id_file = 0

all_columns = cb.get_columns()

patients = cb.get_patient_list()

all_files = cb.get_files(1)
files_names = []
for i in all_files:
    files_names.append(cb.get_file_id(i))

correct_file_names = []
for file_name in files_names:
    data = cb.bulk_data_get(["json_status"], "cardio_file.id=" + str(file_name))
    status = data['data']

    if len(status) > 0:
        if status[0][0] == 'done' or status[0][0] == 'only_delineation':
            correct_file_names.append(file_name)

ecg_data_path = db_path + '\\delineated_by_doc_ids.txt'
np.savetxt(ecg_data_path, np.transpose(np.array(correct_file_names)), fmt='%d')

columns = ["json_lead_i_p_delineation_doc",
           "json_lead_i_qrs_delineation_doc",
           "json_lead_i_t_delineation_doc",
           "json_lead_ii_p_delineation_doc",
           "json_lead_ii_qrs_delineation_doc",
           "json_lead_ii_t_delineation_doc",
           "json_lead_iii_p_delineation_doc",
           "json_lead_iii_qrs_delineation_doc",
           "json_lead_iii_t_delineation_doc",
           "json_lead_avr_p_delineation_doc",
           "json_lead_avr_qrs_delineation_doc",
           "json_lead_avr_t_delineation_doc",
           "json_lead_avl_p_delineation_doc",
           "json_lead_avl_qrs_delineation_doc",
           "json_lead_avl_t_delineation_doc",
           "json_lead_avf_p_delineation_doc",
           "json_lead_avf_qrs_delineation_doc",
           "json_lead_avf_t_delineation_doc",
           "json_lead_v1_p_delineation_doc",
           "json_lead_v1_qrs_delineation_doc",
           "json_lead_v1_t_delineation_doc",
           "json_lead_v2_p_delineation_doc",
           "json_lead_v2_qrs_delineation_doc",
           "json_lead_v2_t_delineation_doc",
           "json_lead_v3_p_delineation_doc",
           "json_lead_v3_qrs_delineation_doc",
           "json_lead_v3_t_delineation_doc",
           "json_lead_v4_p_delineation_doc",
           "json_lead_v4_qrs_delineation_doc",
           "json_lead_v4_t_delineation_doc",
           "json_lead_v5_p_delineation_doc",
           "json_lead_v5_qrs_delineation_doc",
           "json_lead_v5_t_delineation_doc",
           "json_lead_v6_p_delineation_doc",
           "json_lead_v6_qrs_delineation_doc",
           "json_lead_v6_t_delineation_doc"]

for column_id in range(0, len(columns)):

    column = columns[column_id]

    for file_name in correct_file_names:

        data = cb.bulk_data_get([column], "cardio_file.id=" + str(file_name))

        records_ids = data['id']
        ecg_data = data['data']

        for i in range(0, len(records_ids)):

            record_id = records_ids[i]

            record_name = "record_" + str(record_id)

            if column[-17] == 's':
                lead_name = column[5:-20]
            else:
                lead_name = column[5:-18]

            print("lead: ", lead_name, " record: ", record_name)

            record_path = db_path + '\\' + record_name
            if not os.path.exists(record_path):
                os.makedirs(record_path)

            lead_path = record_path + '\\' + lead_name
            if not os.path.exists(lead_path):
                os.makedirs(lead_path)

            del_name = column[5:]
            del_name = del_name.replace(lead_name + '_', '')

            del_data = ecg_data[i][0]
            sort_data = sorted(del_data,key=lambda l:l[1])

            ecg_data_path = lead_path + '\\' + del_name + '.txt'
            np.savetxt(ecg_data_path, sort_data, fmt='%d')
