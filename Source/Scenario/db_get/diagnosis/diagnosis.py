from Source.CardioBase.cardiobase import Cardiobase
from Source.Model.main.ecg.ecg import *
import codecs

DBConfig.name = 'UNNCyberHeartDatabase'
DBConfig.root = 'pyecgdel'
DBConfig.data_catalogue = 'Data'

DBConfig.config_params = 'properties.txt'
DBConfig.p_params = 'p_params.txt'
DBConfig.qrs_params = 'qrs_params.txt'
DBConfig.t_params = 't_params.txt'
DBConfig.filter_params = 'filter_params.txt'
DBConfig.flutter_params = 'flutter_params.txt'

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

for file_name in correct_file_names:

    data = cb.get_diagnosis(file_name)

    record_name = "record_" + str(file_name)

    print("record: ", record_name)

    record_path = db_path + '\\' + record_name
    if not os.path.exists(record_path):
        os.makedirs(record_path)

    ecg_data_path = record_path + '\\diagnosis.txt'

    writefile = codecs.open(ecg_data_path, 'w', 'utf-8')
    writefile.write(data)
    writefile.close()

