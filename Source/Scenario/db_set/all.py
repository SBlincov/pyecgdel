import sys

from Source.Model.main.ecg.ecg import *
from Source.CardioBase.cardiobase import Cardiobase
from Source.Scenario.db_set.set_record import set_record
from Source.Model.main.plot_data.qrs import *
import os

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

cb = Cardiobase()
cb.connect()

leads_names = ConfigParams['LEADS_NAMES']
flutter_leads_names = FlutterParams['LEADS_NAMES']

columns_names = []

for lead_name in leads_names:
    columns_names.append("json_" + lead_name + "_filtrated")

    columns_names.append("json_" + lead_name + "_p_delineation")
    columns_names.append("json_" + lead_name + "_qrs_delineation")
    columns_names.append("json_" + lead_name + "_t_delineation")

    if lead_name in flutter_leads_names:
        columns_names.append("json_" + lead_name + "_flutter_delineation")

    columns_names.append("json_" + lead_name + "_p_morphology")
    columns_names.append("json_" + lead_name + "_qrs_morphology")
    columns_names.append("json_" + lead_name + "_t_morphology")

    columns_names.append("json_" + lead_name + "_characteristics")

    for plot_data_name in QRSPlotDataNames:
        column_name = "json_" + lead_name + "_" + plot_data_name.value
        columns_names.append(column_name)

records_names = []

for record_name in os.listdir(DBConfig.get_db_path()):
    if os.path.isdir(os.path.join(DBConfig.get_db_path(), record_name)):
        records_names.append(record_name)

loaded_file_name = (os.path.join(DBConfig.get_db_path(), "loaded.txt"))
loaded_file = open(loaded_file_name)
loaded = loaded_file.read().splitlines()
loaded_file.close()

num_records = len(records_names)

for record_name in records_names:

    if record_name not in loaded:

        set_record(record_name, cb, columns_names)

        loaded_file = open(loaded_file_name, "a")
        loaded_file.write(record_name + '\n')
        loaded_file.close()