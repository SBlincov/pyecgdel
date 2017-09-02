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

cb = Cardiobase()
cb.connect()

leads_names = ConfigParams['LEADS_NAMES']

columns_names = []

for lead_name in leads_names:
    columns_names.append("json_" + lead_name + "_p_morphology")
    columns_names.append("json_" + lead_name + "_p_morphology_doc")
    columns_names.append("json_" + lead_name + "_qrs_morphology")
    columns_names.append("json_" + lead_name + "_qrs_morphology_doc")
    columns_names.append("json_" + lead_name + "_t_morphology")
    columns_names.append("json_" + lead_name + "_t_morphology_doc")

record_name = 'record_2843'

d = {}
local_path = DBConfig.get_db_path() + "\\" + record_name + "\\"

file_id = int(record_name[7:])

data = cb.bulk_data_get(columns_names, "device_model='AT-101' AND cardio_file.id=" + str(file_id))
if len(data['data']) is not 0:
    for column_name in columns_names:
        cb.delete(file_id, column_name)

if file_id is not -1:
    print(': file_id: ', file_id)

    for lead in cb.leads:
        print(lead)

        d["json_lead_" + lead + "_p_morphology"] = [(file_id, [])]
        d["json_lead_" + lead + "_p_morphology_doc"] = [(file_id, [])]

        qrs_morphs_path = local_path + '/lead_' + lead + '/qrs_morphology.txt'
        lines = [line.rstrip('\n') for line in open(qrs_morphs_path)]
        qrs_records = []
        for line in lines:
            qrs_m = line.split()
            qrs_records.append(qrs_m[0:5])

        d["json_lead_" + lead + "_qrs_morphology"] = [(file_id, qrs_records)]
        d["json_lead_" + lead + "_qrs_morphology_doc"] = [(file_id, qrs_records)]

        d["json_lead_" + lead + "_t_morphology"] = [(file_id, [])]
        d["json_lead_" + lead + "_t_morphology_doc"] = [(file_id, [])]

        print("\n")

    cb.bulk_data_set(d)
    cb.commit()
    print("\n")
    print("\n")
