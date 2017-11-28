import sys

from Source.Model.main.ecg.ecg import *
from Source.CardioBase.cardiobase import Cardiobase
from Source.Scenario.db_set.set_record import set_record

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

record_name = "record_2319"

cb = Cardiobase()
cb.connect()

leads_names = ConfigParams['LEADS_NAMES']

columns_names = []

for lead_name in leads_names:
    columns_names.append("json_" + lead_name + "_filtrated")

    columns_names.append("json_" + lead_name + "_p_delineation")
    columns_names.append("json_" + lead_name + "_qrs_delineation")
    columns_names.append("json_" + lead_name + "_t_delineation")

    columns_names.append("json_" + lead_name + "_p_morphology")
    columns_names.append("json_" + lead_name + "_qrs_morphology")
    columns_names.append("json_" + lead_name + "_t_morphology")

    columns_names.append("json_" + lead_name + "_characteristics")


set_record(record_name, cb, columns_names)

