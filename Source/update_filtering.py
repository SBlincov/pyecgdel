import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "..\\..\\..\\..\\bin"))
from cardiobase import Cardiobase
from Source.Model.main.ecg.ecg import *


def _main(cb, id_file):
    print("id = " + str(id_file))
    leads_names = ConfigParams['LEADS_NAMES']
    columns_names = []
    for lead_name in leads_names:
        columns_names.append("json_" + lead_name + "_original")
    data = cb.bulk_data_get(columns_names, "cardio_file.id=" + str(id_file))
    ecg_data = data['data']

    ecg_input_data_dict = dict()
    result_data_dict = dict()
    result_columns_names = []

    for lead_name_id in range(0, len(leads_names)):
        if ecg_data[0][lead_name_id] is not None:
            ecg_input_data_dict[leads_names[lead_name_id]] = ecg_data[0][lead_name_id]

    ecg = ECG(ecg_input_data_dict)
    ecg.cwt_filtration()
    ecg.dwt()
    ecg.delineation()
    ##ecg.add_delineation_data_to_dict(result_data_dict, result_columns_names, id_file)
    ##ecg.add_morphology_data_to_dict(result_data_dict, result_columns_names, id_file)
    #ecg.characteristics()
    ##ecg.add_characteristics_data_to_dict(result_data_dict, result_columns_names, id_file)

    ecg.adaptive_filtration()
    ecg.add_filter_data_to_dict(result_data_dict, result_columns_names, id_file)
    for lead_name in leads_names:
        cb.delete(id_file, "json_" + lead_name + "_filtrated")
    cb.commit()

    cb.bulk_data_set(result_data_dict)
    cb.commit()
    cb.cardio_event("FEATURES", "DELINEATION_DONE", id_file)


if __name__ == "__main__":
    cb = Cardiobase()
    cb.connect()
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

    ids_october = [50436612, 50436671, 50436730, 50436790, 50437115, 50436937, 50436996,
                   50437056, 50437173, 50437233, 1102526720, 1102526384, 1102526300,
                   1102526468, 1102526216, 1102526636, 1102526552, 50438357, 50440535,
                   1102528543, 1102527784, 1102528291, 1102528375, 1102528459,
                   50442152, 50488354, 1102528207, 1102528036, 1102527952,
                   1102527868, 50441851, 1102528627, 50441792, 50442000, 50488538,
                   50444877, 50488476, 50488416, 50444937, 50448183, 50448422,
                   50448481, 50448540, 50448599, 50448651, 50448710, 1102530490,
                   1102530574, 1102530745, 1102530830, 1102530906, 1102531056,
                   1102531161, 1102531245, 1102531329, 50488600, 50488662, 50448859,
                   50451655, 50451714, 50451773, 50488810, 50488872, 50455077,
                   50455332, 50455427, 50455489, 50488996, 50489058, 50489120,
                   50489182, 50489244, 1102546985, 1102547069, 50489306,
                   50489368, 50489430, 50459757, 50459816, 50459875, 1102546229,
                   1102546145, 1102546061, 1102546901, 1102545977, 1102545893,
                   1102545809, 1102545725, 1102545641, 1102545554, 1102545384,
                   1102545300, 1102545216, 1102545132, 1102545048, 1102544964,
                   1102544880, 1102544792, 1102544708, 50460111, 1102545470,
                   1102546817, 1102546733, 1102546649, 1102546565, 1102546481, 
                   1102546397, 1102546313, 50464197, 50477113, 50477165, 
                   1102547279, 1102547363, 1102547513, 1102547609, 1102547693,
                   1102547808, 50489535, 50489597, 50489659, 50489713,
                   50489775, 50489880, 50489942, 50490004, 50476664, 50476723,
                   50476782, 50476841, 50476900, 50483728, 50483780,
                   50490066, 50490128, 50490190, 50490252, 50490314,
                   50488092, 50488175, 50488236, 50488295, 1102555618, 1102555723,
                   1102555807, 1102555989, 1102556065, 1102556149, 1102555300,
                   1102555384, 1102555468, 1102556311, 1102556426, 50494292,
                   50494351, 50494410, 50494469]
    ids = ids_october
    wrong_ids = []
    for file_id in ids:
        try:
            _main(cb, file_id)
        except:
            wrong_ids.append(file_id)
    print("Records with errors (probably, wrong ids):")
    print(wrong_ids)
    cb.disconnect()
