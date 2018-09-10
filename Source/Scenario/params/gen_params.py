import sys

from Source.Model.main.ecg.ecg import *
from Source.CardioBase.cardiobase import Cardiobase
import json

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

config_params = ConfigParams
p_params = PParams
qrs_params = QRSParams
t_params = TParams
filter_params = FilterParams
flutter_params = FlutterParams

params = {}
params["config"] = config_params
params["filter"] = filter_params
params["flutter"] = flutter_params
params["p"] = p_params
params["qrs"] = qrs_params
params["t"] = t_params

with open("params.json", 'w') as f:
    json.dump(params, f, indent=4, sort_keys=True)