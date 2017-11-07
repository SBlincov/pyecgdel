import sys

sys.path.append('..\\..\\libs\\cardiobase')
from Source.CardioBase.cardiobase import Cardiobase
from Source.Model.main.ecg.ecg import *

cb = Cardiobase()
cb.connect()

id_file = 3066

params_hash = cb.get_hash(24)

config_params_from_hash = params_hash['data'][params_hash['id'].index(0)]
p_params_from_hash = params_hash['data'][params_hash['id'].index(1)]
qrs_params_from_hash = params_hash['data'][params_hash['id'].index(2)]
t_params_from_hash = params_hash['data'][params_hash['id'].index(3)]
filter_params_from_hash = params_hash['data'][params_hash['id'].index(4)]

init_params(config_params_from_hash, ParamsType.config_params)
init_params(p_params_from_hash, ParamsType.p_params)
init_params(qrs_params_from_hash, ParamsType.qrs_params)
init_params(t_params_from_hash, ParamsType.t_params)
init_params(filter_params_from_hash, ParamsType.filter_params)

leads_names = ConfigParams['LEADS_NAMES']

columns_names = []
for lead_name in leads_names:
    columns_names.append("json_" + lead_name + "_original")

data = cb.bulk_data_get(columns_names, "cardio_file.id=" + str(id_file))
ecg_data = data['data']

leads_names_exist = []
leads_ids_exist = []
for lead_id in range(0, len(leads_names)):
    lead_data = ecg_data[0][lead_id]
    if lead_data is not None:
        leads_names_exist.append(leads_names[lead_id])
        leads_ids_exist.append(lead_id)

leads_names = leads_names_exist

ecg_input_data_dict = dict()
result_data_dict = dict()
result_columns_names = []

for lead_name_id in range(0, len(leads_names)):
    if ecg_data[0][lead_name_id] is not None:
        ecg_input_data_dict[leads_names[lead_name_id]] = ecg_data[0][lead_name_id]

ecg = ECG(ecg_input_data_dict)
ecg.cwt_filtration()
# For now the filtering used for delineation is internal to this module
# and filtering for output is done separately later
#ecg.add_filtrated_data_to_dict(result_data_dict, result_columns_names, id_file)
ecg.dwt()
ecg.delineation()
ecg.add_delineation_data_to_dict(result_data_dict, result_columns_names, id_file)
ecg.add_morphology_data_to_dict(result_data_dict, result_columns_names, id_file)
ecg.characteristics()
ecg.add_characteristics_data_to_dict(result_data_dict, result_columns_names, id_file)
# Adaptive filtering
ecg.adaptive_filtration()
ecg.add_filter_data_to_dict(result_data_dict, result_columns_names, id_file)

cb.bulk_data_set(result_data_dict)
cb.commit()

cb.cardio_event("FEATURES", "DELINEATION_DONE", id_file)

cb.disconnect()
