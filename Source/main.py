from Source.Model.main.ecg.ecg import *
from Source.CardioBase.cardiobase import Cardiobase

id_file = 1007

cb = Cardiobase()
cb.connect()

params_hash = cb.get_hash(24)

config_params_from_hash = params_hash['data'][0]
p_params_from_hash = params_hash['data'][1]
qrs_params_from_hash = params_hash['data'][2]
t_params_from_hash = params_hash['data'][3]
filter_params_from_hash = params_hash['data'][4]

init_params(config_params_from_hash, ParamsType.config_params)
init_params(p_params_from_hash, ParamsType.p_params)
init_params(qrs_params_from_hash, ParamsType.qrs_params)
init_params(t_params_from_hash, ParamsType.t_params)
init_params(filter_params_from_hash, ParamsType.filter_params)

leads_names = ConfigParams['LEADS_NAMES']

all_columns_names = []
for lead_name in leads_names:
    all_columns_names.append(lead_name + "_original")

data = cb.bulk_data_get(all_columns_names, "id_file=" + str(id_file))
ecg_data = data['data']

ecg_input_data_dict = dict()
result_data_dict = dict()
result_columns_names = []

for lead_name_id in range(0, len(leads_names)):
    if ecg_data[0][lead_name_id] is not None:
        ecg_input_data_dict[leads_names[lead_name_id]] = ecg_data[0][lead_name_id]

ecg = ECG(ecg_input_data_dict)
ecg.cwt_filtration()
ecg.add_filtrated_data_to_dict(result_data_dict, result_columns_names, id_file)
ecg.dwt()
ecg.delineation()
ecg.add_delineation_data_to_dict(result_data_dict, result_columns_names, id_file)
ecg.characteristics()
ecg.add_characteristics_data_to_dict(result_data_dict, result_columns_names, id_file)

cb.bulk_data_set(result_data_dict)
cb.commit()

#cb.cardio_event("FEATURES", "DELINEATION_DONE", id_file)

cb.disconnect()
