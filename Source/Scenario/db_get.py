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

columns = ["lead_i_original",
           "lead_ii_original",
           "lead_iii_original",
           "lead_avr_original",
           "lead_avl_original",
           "lead_avf_original",
           "lead_v1_original",
           "lead_v2_original",
           "lead_v3_original",
           "lead_v4_original",
           "lead_v5_original",
           "lead_v6_original"]

for column_id in range(0, len(columns)):

    column = columns[column_id]

    #data = cb.bulk_data_get([column], "device_model='AT-101' AND id_file>" + str(max_id_file))
    data = cb.bulk_data_get([column], "device_model='AT-101'")
    records_ids = data['id']
    ecg_data = data['data']

    for i in range(0, len(records_ids)):

        record_id = records_ids[i]

        record_name = "record_" + str(record_id)
        lead_name = column[:-9]

        print("lead: ", lead_name, " record: ", record_name)

        record_path = db_path + '\\' + record_name
        if not os.path.exists(record_path):
            os.makedirs(record_path)

        lead_path = record_path + '\\' + lead_name
        if not os.path.exists(lead_path):
            os.makedirs(lead_path)

        ecg_data_path = lead_path + '\\original.txt'
        np.savetxt(ecg_data_path, np.transpose(np.array(ecg_data[i])), fmt='%d')
