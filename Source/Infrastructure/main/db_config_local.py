import os

from .config import *
from ...Model.main.data_details.ecg_data_details import *


class ParamsType(Enum):
    config_params = 0
    p_params = 1
    qrs_params = 2
    t_params = 3
    filter_params = 4


class DBConfig:

    name = 'mukhina'
    root = 'pyecgdel'
    data_catalogue = 'Data'

    config_params = 'properties.txt'
    p_params = 'p_params.txt'
    qrs_params = 'qrs_params.txt'
    t_params = 't_params.txt'
    filter_params = 'filter_params.txt'

    @staticmethod
    def get_db_path():

        base_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = base_dir.split(DBConfig.root, 1)[0] + DBConfig.root
        path = base_dir + '\\' + DBConfig.data_catalogue + '\\' + DBConfig.name

        return path

    @staticmethod
    def get_db_params_path(params_type=ParamsType.config_params):

        db_path = DBConfig.get_db_path()
        path = db_path + '\\'
        if params_type is ParamsType.config_params:
            path += DBConfig.config_params
        elif params_type is ParamsType.p_params:
            path += DBConfig.p_params
        elif params_type is ParamsType.qrs_params:
            path += DBConfig.qrs_params
        elif params_type is ParamsType.t_params:
            path += DBConfig.t_params
        elif params_type is ParamsType.filter_params:
            path += DBConfig.filter_params

        return path

    @staticmethod
    def get_db_lead_path(patient_name, record_name, lead_name, details):

        if not isinstance(details, ECGDataDetails):
            raise InvalidECGDataDetails('details must be ECGDataDetails instance')

        db_path = DBConfig.get_db_path()
        if patient_name:
            path = db_path + '\\' + patient_name + '\\' + record_name + '\\' + lead_name + '\\' + details.name + ConfigParams['EXTENSION']
        else:
            path = db_path + '\\' + record_name + '\\' + lead_name + '\\' + details.name + ConfigParams['EXTENSION']

        return path
