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
    columns_names.append("json_" + lead_name + "_filtrated")
    columns_names.append("json_" + lead_name + "_p_delineation")
    columns_names.append("json_" + lead_name + "_p_delineation_doc")
    columns_names.append("json_" + lead_name + "_qrs_delineation")
    columns_names.append("json_" + lead_name + "_qrs_delineation_doc")
    columns_names.append("json_" + lead_name + "_t_delineation")
    columns_names.append("json_" + lead_name + "_t_delineation_doc")
    columns_names.append("json_" + lead_name + "_characteristics")


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

        filtrated = np.loadtxt(local_path + '/lead_' + lead + '/filtrated.txt')
        d["json_lead_" + lead + "_filtrated"] = [(file_id, filtrated.tolist())]

        p_delineation = np.loadtxt(local_path + '/lead_' + lead + '/p_delineation.txt', dtype=np.int)
        print("p_del shape: ", p_delineation.shape)
        if len(p_delineation) is 0:
            d["json_lead_" + lead + "_p_delineation"] = [(file_id, [])]
            d["json_lead_" + lead + "_p_delineation_doc"] = [(file_id, [])]
        elif len(p_delineation) is 1:
            d["json_lead_" + lead + "_p_delineation"] = [(file_id, [p_delineation.tolist()])]
            d["json_lead_" + lead + "_p_delineation_doc"] = [(file_id, [p_delineation.tolist()])]
        else:
            d["json_lead_" + lead + "_p_delineation"] = [(file_id, p_delineation.tolist())]
            d["json_lead_" + lead + "_p_delineation_doc"] = [(file_id, p_delineation.tolist())]

        qrs_delineation = np.loadtxt(local_path + '/lead_' + lead + '/qrs_delineation.txt', dtype=np.int)
        print("qrs_del shape: ", qrs_delineation.shape)
        if len(qrs_delineation) is 0:
            d["json_lead_" + lead + "_qrs_delineation"] = [(file_id, [])]
            d["json_lead_" + lead + "_qrs_delineation_doc"] = [(file_id, [])]
        elif len(qrs_delineation) is 1:
            d["json_lead_" + lead + "_qrs_delineation"] = [(file_id, [qrs_delineation.tolist()])]
            d["json_lead_" + lead + "_qrs_delineation_doc"] = [(file_id, [qrs_delineation.tolist()])]
        else:
            d["json_lead_" + lead + "_qrs_delineation"] = [(file_id, qrs_delineation.tolist())]
            d["json_lead_" + lead + "_qrs_delineation_doc"] = [(file_id, qrs_delineation.tolist())]

        t_delineation = np.loadtxt(local_path + '/lead_' + lead + '/t_delineation.txt', dtype=np.int)
        print("t_del shape: ", t_delineation.shape)
        if len(t_delineation) is 0:
            d["json_lead_" + lead + "_t_delineation"] = [(file_id, [])]
            d["json_lead_" + lead + "_t_delineation_doc"] = [(file_id, [])]
        elif len(t_delineation) is 1:
            d["json_lead_" + lead + "_t_delineation"] = [(file_id, [t_delineation.tolist()])]
            d["json_lead_" + lead + "_t_delineation_doc"] = [(file_id, [t_delineation.tolist()])]
        else:
            d["json_lead_" + lead + "_t_delineation"] = [(file_id, t_delineation.tolist())]
            d["json_lead_" + lead + "_t_delineation_doc"] = [(file_id, t_delineation.tolist())]

        print("\n")

        char_path = local_path + '/lead_' + lead + '/characteristics.txt'
        lines = [line.rstrip('\n') for line in open(char_path)]
        ch_names = []
        ch_values = []
        for line in lines:
            ch = line.split()
            ch_names.append(ch[0])
            if (ch[1]) != 'n':
                ch_values.append(float(ch[1]))
            else:
                ch_values.append(None)
        d["json_lead_" + lead + "_characteristics"] = [(file_id, [ch_names, ch_values])]

    cb.bulk_data_set(d)
    cb.commit()
    print("\n")
    print("\n")
