import sys

from Source.Model.main.ecg.ecg import *
from Source.CardioBase.cardiobase import Cardiobase

DBConfig.name = 'sarov'
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

hash_data_config_params = ConfigParams
hash_data_p_params = PParams
hash_data_qrs_params = QRSParams
hash_data_t_params = TParams
hash_data_filter_params = FilterParams
hash_data_flutter_params = FlutterParams

#id_hash_params = 24
id_hash_params = 656
num_inserted_rows_config_params = cb.update_hash_row_data(id_hash_params, 0, hash_data_config_params)
num_inserted_rows_p_params = cb.update_hash_row_data(id_hash_params, 1, hash_data_p_params)
num_inserted_rows_qrs_params = cb.update_hash_row_data(id_hash_params, 2, hash_data_qrs_params)
num_inserted_rows_t_params = cb.update_hash_row_data(id_hash_params, 3, hash_data_t_params)
num_inserted_rows_filter_params = cb.update_hash_row_data(id_hash_params, 4, hash_data_filter_params)
num_inserted_rows_flutter_params = cb.update_hash_row_data(id_hash_params, 5, hash_data_flutter_params)
cb.commit()
cb.disconnect()

