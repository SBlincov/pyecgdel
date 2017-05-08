from Source.Model.main.ecg.ecg import *
from Source.Infrastructure.main.db_config_local import *


DBConfig.name = 'shiller'
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


ConfigParams['LEADS_NAMES'] = ['lead_avl']

record_id = 2334

record_name = "record_" + str(record_id)

print('Record Name: ', record_name)
ecg = ECG(data=LOCAL_DB, name=None, record=record_name)
ecg.cwt_filtration()
ecg.save_data_local(ECGDataDetails.filtrated)
ecg.dwt()
ecg.save_data_local(ECGDataDetails.wdc)
ecg.delineation()
ecg.save_data_local(ECGDataDetails.qrs_delineation)
ecg.save_data_local(ECGDataDetails.qrs_morphology)
ecg.save_data_local(ECGDataDetails.p_delineation)
ecg.save_data_local(ECGDataDetails.t_delineation)

ecg.characteristics()
ecg.save_data_local(ECGDataDetails.characteristics)
