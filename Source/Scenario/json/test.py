import json
import sys

from Source.Model.main.ecg.ecg import *
from Source.CardioBase.cardiobase import Cardiobase

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

record_id = 2517
record_name = 'record_' + str(record_id)

json_file = open('signal_' + str(record_id) + '_float.json')
json_str = json_file.read()
signals = json.loads(json_str)

ecg = ECG(data=signals, name=None, record=record_name)

delineation = ecg.get_delineation()
morphology = ecg.get_morphology()
filtrated = ecg.get_filtrated()
characteristics = ecg.get_characteristics()
plot_data = ecg.get_plot_data()

# ecg._cwt_filtration()
# ecg._save_local(ECGDataDetails.filtrated)
# ecg._dwt()
# ecg._save_local(ECGDataDetails.wdc)
# ecg._delineation()
# ecg._adaptive_filtration()
# ecg._del_correction()
# ecg._characteristics()
# ecg._init_plot_data()
#
# ecg._save_local(ECGDataDetails.qrs_delineation)
# ecg._save_local(ECGDataDetails.qrs_morphology)
#
# ecg._save_local(ECGDataDetails.t_delineation)
# ecg._save_local(ECGDataDetails.t_morphology)
#
# ecg._save_local(ECGDataDetails.p_delineation)
# ecg._save_local(ECGDataDetails.p_morphology)
#
# ecg._save_local(ECGDataDetails.flutter_delineation)
#
# ecg._save_local(ECGDataDetails.adaptive_filtrated)
#
# ecg._save_local(ECGDataDetails.characteristics)
#
# ecg._save_local(ECGDataDetails.qrs_plot_data)


print('Done')
