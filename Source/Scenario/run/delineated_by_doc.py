from Source.Model.main.ecg.ecg import *
from Source.Infrastructure.main.db_config_local import *
from Source.Scenario.run.record import run_record

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

db_path = DBConfig.get_db_path()
fn_dd = db_path + '\\delineated_by_doc_ids.txt'
dd_ids = np.loadtxt(fn_dd, dtype=int)

records_ids = dd_ids.tolist()
records_names = []
for record_id in records_ids:
    record_name = 'record_' + str(record_id)
    records_names.append(record_name)

for record_name in records_names:
   run_record(record_name)
