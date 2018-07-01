from Source.Model.main.ecg.ecg import *
import os.path
import json


def _get_params(sample_rate):
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
    file_name = 'params_default.json'
    if sample_rate == 250:
        file_name = 'params_sarov.json'
    path = os.path.join(__location__, file_name)
    with open(path, 'r') as f:
        return json.loads(f.read())


def ecg_from_signals(signals, sample_rate):
    params = _get_params(sample_rate)

    config_params_from_hash = params['config']
    p_params_from_hash = params['p']
    qrs_params_from_hash = params['qrs']
    t_params_from_hash = params['t']
    filter_params_from_hash = params['filter']
    flutter_params_from_hash = params['flutter']

    init_params(config_params_from_hash, ParamsType.config_params)
    init_params(p_params_from_hash, ParamsType.p_params)
    init_params(qrs_params_from_hash, ParamsType.qrs_params)
    init_params(t_params_from_hash, ParamsType.t_params)
    init_params(filter_params_from_hash, ParamsType.filter_params)
    init_params(flutter_params_from_hash, ParamsType.flutter_params)

    return ECG(signals)