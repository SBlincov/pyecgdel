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

init_params(params_type=ParamsType.config_params)
init_params(params_type=ParamsType.p_params)
init_params(params_type=ParamsType.qrs_params)
init_params(params_type=ParamsType.t_params)
init_params(params_type=ParamsType.filter_params)

cb = Cardiobase()
cb.connect()

hash_data_config_params = ConfigParams
hash_data_p_params = PParams
hash_data_qrs_params = QRSParams
hash_data_t_params = TParams
hash_data_filter_params = FilterParams

id_type_hash = cb.create_type_hash('sarov')
num_inserted_rows_config_params = cb.insert_hash_row(id_type_hash, 0, 'config', hash_data_config_params)
num_inserted_rows_p_params = cb.insert_hash_row(id_type_hash, 1, 'p', hash_data_p_params)
num_inserted_rows_qrs_params = cb.insert_hash_row(id_type_hash, 2, 'qrs', hash_data_qrs_params)
num_inserted_rows_t_params = cb.insert_hash_row(id_type_hash, 3, 't', hash_data_t_params)
num_inserted_rows_filter_params = cb.insert_hash_row(id_type_hash, 4, 'filter', hash_data_filter_params)
cb.commit()
cb.disconnect()

