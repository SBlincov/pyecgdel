from Source.Model.main.ecg.ecg import *
from Source.Infrastructure.main.db_config_local import *

DBConfig.name = 'qtdb'
DBConfig.root = 'pyecgdel'
DBConfig.data_catalogue = 'Data'

DBConfig.config_params = 'properties.txt'
DBConfig.p_params = 'p_params.txt'
DBConfig.qrs_params = 'qrs_params.txt'
DBConfig.t_params = 't_params.txt'
DBConfig.filter_params = 'filter_params.txt'

init_params(params_type=ParamsType.config_params)
init_params(params_type=ParamsType.p_params)
init_params(params_type=ParamsType.qrs_params)
init_params(params_type=ParamsType.t_params)
init_params(params_type=ParamsType.filter_params)

records_names = []

for record_name in os.listdir(DBConfig.get_db_path()):
    if os.path.isdir(os.path.join(DBConfig.get_db_path(), record_name)):
        records_names.append(record_name)

# records_names = ['record_1',
#                  'record_2',
#                  'record_3',
#                  'record_4',
#                  'record_5',
#                  'record_6',
#                  'record_7',
#                  'record_8',
#                  'record_9',
#                  'record_10',
#                  'record_11',
#                  'record_12',
#                  'record_13',
#                  'record_14',
#                  'record_15',
#                  'record_16',
#                  'record_17',
#                  'record_18',
#                  'record_19',
#                  'record_20'
#                  ]

for record_name in records_names:
    print('Record Name: ', record_name)
    ecg = ECG(data=LOCAL_DB, name=None, record=record_name)
    ecg.cwt_filtration()
    ecg.save_data_local(ECGDataDetails.filtrated)
    ecg.dwt()
    ecg.save_data_local(ECGDataDetails.wdc)
    ecg.delineation()
    ecg.save_data_local(ECGDataDetails.qrs_delineation)
    ecg.save_data_local(ECGDataDetails.p_delineation)
    ecg.save_data_local(ECGDataDetails.t_delineation)

    ecg.characteristics()
    ecg.save_data_local(ECGDataDetails.characteristics)
