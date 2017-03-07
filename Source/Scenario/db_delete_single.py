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

init_params(params_type=ParamsType.config_params)
init_params(params_type=ParamsType.p_params)
init_params(params_type=ParamsType.qrs_params)
init_params(params_type=ParamsType.t_params)
init_params(params_type=ParamsType.filter_params)

id_file = 703

cb = Cardiobase()
cb.connect()

leads_names = ConfigParams['LEADS_NAMES']

columns_names = []

for lead_name in leads_names:
    columns_names.append(lead_name + "_filtrated")
    columns_names.append(lead_name + "_p_delineation")
    columns_names.append(lead_name + "_qrs_delineation")
    columns_names.append(lead_name + "_t_delineation")
    columns_names.append(lead_name + "_characteristics")

data = cb.bulk_data_get(columns_names, "id_file=" + str(id_file))

for column_name in columns_names:
    cb.delete(id_file, column_name)
