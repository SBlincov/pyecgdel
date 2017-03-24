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

columns = ["json_R_QRS_ON",
           "json_R_QRS_OFF",
           "json_R_P_ON",
           "json_R_T_OFF"]

for column_id in range(0, len(columns)):

    column = columns[column_id]

    #data = cb.bulk_data_get([column], "device_model='AT-101' AND id_file>" + str(max_id_file))
    data = cb.bulk_data_get([column], "device_model='AT-101'")
    records_ids = data['id']
    ecg_data = data['data']

    for i in range(0, len(records_ids)):

        record_id = records_ids[i]

        record_name = "record_" + str(record_id)

        record_path = db_path + '\\' + record_name
        if not os.path.exists(record_path):
            os.makedirs(record_path)

        original_del_path = record_path + '\\' + 'original_del'
        if not os.path.exists(original_del_path):
            os.makedirs(original_del_path)

        ecg_data_path = original_del_path + '\\' + str(column) + '.txt'
        np.savetxt(ecg_data_path, np.transpose(np.array(ecg_data[i])), fmt='%0.4f')
