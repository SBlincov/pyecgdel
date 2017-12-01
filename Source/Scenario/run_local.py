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

records_names = []

for record_name in os.listdir(DBConfig.get_db_path()):
    if os.path.isdir(os.path.join(DBConfig.get_db_path(), record_name)):
        records_names.append(record_name)

for record_name in records_names:
    print('Record Name: ', record_name)
    ecg = ECG(data=LOCAL_DB, name=None, record=record_name)
    ecg.cwt_filtration()
    ecg.save_local(ECGDataDetails.filtrated)
    ecg.dwt()
    ecg.save_local(ECGDataDetails.wdc)
    ecg.delineation()
    ecg.adaptive_filtration()
    ecg.del_correction()
    ecg.characteristics()
    ecg.init_plot_data()

    ecg.save_local(ECGDataDetails.qrs_delineation)
    ecg.save_local(ECGDataDetails.qrs_morphology)

    ecg.save_local(ECGDataDetails.t_delineation)
    ecg.save_local(ECGDataDetails.t_morphology)

    ecg.save_local(ECGDataDetails.p_delineation)
    ecg.save_local(ECGDataDetails.p_morphology)

    ecg.save_local(ECGDataDetails.adaptive_filtrated)

    ecg.save_local(ECGDataDetails.characteristics)

