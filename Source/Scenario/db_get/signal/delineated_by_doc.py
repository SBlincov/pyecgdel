from Source.CardioBase.cardiobase import Cardiobase
from Source.Model.main.ecg.ecg import *

DBConfig.name = 'shiller'
DBConfig.root = 'pyecgdel'
DBConfig.data_catalogue = 'Data'

DBConfig.config_params = 'properties.txt'
DBConfig.p_params = 'p_params.txt'
DBConfig.qrs_params = 'qrs_params.txt'
DBConfig.t_params = 't_params.txt'
DBConfig.filter_params = 'filter_params.txt'

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

columns = ["json_lead_i_original",
           "json_lead_ii_original",
           "json_lead_iii_original",
           "json_lead_avr_original",
           "json_lead_avl_original",
           "json_lead_avf_original",
           "json_lead_v1_original",
           "json_lead_v2_original",
           "json_lead_v3_original",
           "json_lead_v4_original",
           "json_lead_v5_original",
           "json_lead_v6_original"]

for column_id in range(0, len(columns)):

    column = columns[column_id]

    for file_name in correct_file_names:

        data = cb.bulk_data_get([column], "cardio_file.id=" + str(file_name))
        #data = cb.bulk_data_get([column], "device_model='AT-101'")
        records_ids = data['id']
        ecg_data = data['data']

        for i in range(0, len(records_ids)):

            record_id = records_ids[i]

            record_name = "record_" + str(record_id)
            lead_name = column[5:-9]

            print("lead: ", lead_name, " record: ", record_name)

            record_path = db_path + '\\' + record_name
            if not os.path.exists(record_path):
                os.makedirs(record_path)

            lead_path = record_path + '\\' + lead_name
            if not os.path.exists(lead_path):
                os.makedirs(lead_path)

            ecg_data_path = lead_path + '\\original.txt'
            np.savetxt(ecg_data_path, np.transpose(np.array(ecg_data[i])), fmt='%d')
