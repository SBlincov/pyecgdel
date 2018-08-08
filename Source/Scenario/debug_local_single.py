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
DBConfig.flutter_params = 'flutter_params.txt'

init_params(params_type=ParamsType.config_params)
init_params(params_type=ParamsType.p_params)
init_params(params_type=ParamsType.qrs_params)
init_params(params_type=ParamsType.t_params)
init_params(params_type=ParamsType.filter_params)
init_params(params_type=ParamsType.flutter_params)


ConfigParams['LEADS_NAMES'] = ['lead_i']

record_id = 3508

record_name = "record_" + str(record_id)

print('Record Name: ', record_name)
ecg = ECG(data=LOCAL_DB, name=None, record=record_name)
ecg._cwt_filtration()
ecg._save_local(ECGDataDetails.filtrated)
ecg._dwt()
ecg._save_local(ECGDataDetails.wdc)
ecg._delineation()
ecg._save_local(ECGDataDetails.qrs_delineation)
ecg._save_local(ECGDataDetails.qrs_morphology)
ecg._save_local(ECGDataDetails.t_delineation)
ecg._save_local(ECGDataDetails.t_morphology)
ecg._save_local(ECGDataDetails.p_delineation)

ecg._characteristics()
ecg._save_local(ECGDataDetails.characteristics)
