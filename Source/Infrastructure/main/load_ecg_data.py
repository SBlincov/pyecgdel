import os

import numpy as np

from ...Model.main.ecg.ecg import *
from ...Infrastructure.main.db_config_local import *
from ...Infrastructure.main.ecg_data_routines import *

from ...Infrastructure.main.config import *
from ...Model.main.params.common import *
from ...Model.main.params.p import *
from ...Model.main.params.qrs import *
from ...Model.main.params.t import *


def init_params(data_dict=LOCAL_DB, params_type=ParamsType.config_params):

    if data_dict is LOCAL_DB:

        params_path = DBConfig.get_db_params_path(params_type)

        if not os.path.isfile(params_path):
            if params_type is ParamsType.config_params:
                raise InvalidECGData('Config params file is not exist')
            elif params_type is ParamsType.p_params:
                raise InvalidECGData('P params file is not exist')
            elif params_type is ParamsType.qrs_params:
                raise InvalidECGData('QRS params file is not exist')
            elif params_type is ParamsType.t_params:
                raise InvalidECGData('T params file is not exist')
            elif params_type is ParamsType.filter_params:
                raise InvalidECGData('Filter params file is not exist')
            else:
                raise InvalidECGData('Unknown params type')

        params_file = open(params_path, 'r')
        params = [line.rstrip().split() for line in params_file]
        params_file.close()

        for param in params:
            if params_type is ParamsType.config_params:
                if param[0] in ConfigParams:
                    if len(param) > 2:
                        ConfigParams[param[0]] = param[1:]
                    else:
                        if param[0] == 'LEADS_NAMES':
                            ConfigParams[param[0]] = [param[1]]
                        else:
                            ConfigParams[param[0]] = param[1]
                else:
                    raise InvalidECGData('Unknown config params keys')

            elif params_type is ParamsType.p_params:
                if param[0] in PParams:
                    PParams[param[0]] = float(param[1])
                else:
                    raise InvalidECGData('Unknown p params keys')

            elif params_type is ParamsType.qrs_params:
                if param[0] in QRSParams:
                    QRSParams[param[0]] = float(param[1])
                else:
                    raise InvalidECGData('Unknown qrs params keys')

            elif params_type is ParamsType.t_params:
                if param[0] in TParams:
                    TParams[param[0]] = float(param[1])
                else:
                    raise InvalidECGData('Unknown t params keys')

            elif params_type is ParamsType.filter_params:
                if param[0] in FilterParams:
                    FilterParams[param[0]] = float(param[1])
                else:
                    raise InvalidECGData('Unknown filter params keys')

    elif isinstance(data_dict, dict):

        for data_dict_key in data_dict:

            if params_type is ParamsType.config_params:
                if data_dict_key in ConfigParams:
                    ConfigParams[data_dict_key] = data_dict[data_dict_key]
                else:
                    raise InvalidECGData('Unknown config params keys')

            elif params_type is ParamsType.p_params:
                if data_dict_key in PParams:
                    PParams[data_dict_key] = data_dict[data_dict_key]
                else:
                    raise InvalidECGData('Unknown p params keys')

            elif params_type is ParamsType.qrs_params:
                if data_dict_key in QRSParams:
                    QRSParams[data_dict_key] = data_dict[data_dict_key]
                else:
                    raise InvalidECGData('Unknown qrs params keys')

            elif params_type is ParamsType.t_params:
                if data_dict_key in TParams:
                    TParams[data_dict_key] = data_dict[data_dict_key]
                else:
                    raise InvalidECGData('Unknown t params keys')

            elif params_type is ParamsType.filter_params:
                if data_dict_key in FilterParams:
                    FilterParams[data_dict_key] = data_dict[data_dict_key]
                else:
                    raise InvalidECGData('Unknown filter params keys')

            else:
                raise InvalidECGData('Unknown params type')

    else:
        raise InvalidECGData('Unknown params data')


def load_ecg_data_local(ecg, details=ECGDataDetails.original):

    sampling_rate = float(ConfigParams['SAMPLING_RATE'])
    leads_names = ConfigParams['LEADS_NAMES']

    print("Init ecg from local database...")

    if details is ECGDataDetails.original:

        leads = []
        for lead_name in leads_names:

            print("Init " + str(lead_name) + "...")

            data_file_name = DBConfig.get_db_lead_path(ecg.name, ecg.record, lead_name, details)

            if not os.path.exists(data_file_name):
                raise InvalidECGData('Lead file is not exist')

            data = np.loadtxt(data_file_name)

            lead = ECGLead(lead_name, data, sampling_rate)
            leads.append(lead)

            print("Init " + str(lead_name) + " complete")

        ecg.leads = leads

    else:

        if len(ecg.leads) is not len(leads_names):
            raise InvalidECGData('Number of existing leads in ecg instance differs from number of leads in database')

        if abs(ecg.leads[0].sampling_rate - sampling_rate) > EPSILON:
            raise InvalidECGData('Sampling rate in current instance must be equal to sampling rate in database')

        for lead_id in range(len(leads_names)):
            if leads_names[lead_id] != ecg.leads[lead_id].name:
                raise InvalidECGData('ECG lead names must be agree with database')

            data_file_name = DBConfig.get_db_lead_path(ecg.name, ecg.record, leads_names[lead_id], details)

            if not os.path.exists(data_file_name):
                raise InvalidECGData('Properties file is not exist')

            data = np.loadtxt(data_file_name)

            if details == ECGDataDetails.wdc:
                ecg.leads[lead_id].wdc = data
            elif details == ECGDataDetails.qrs_delineation:
                ecg.leads[lead_id].qrs_delineations = data
            elif details == ECGDataDetails.p_delineation:
                ecg.leads[lead_id].p_delineations = data
            elif details == ECGDataDetails.t_delineation:
                ecg.leads[lead_id].t_delineations = data
            else:
                raise InvalidECGDataDetails('Error! Invalid ecg details')

    print("Init ecg from local database complete")
    print("")

