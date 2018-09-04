from Source.Model.main.ecg.ecg import *
from Source.Infrastructure.main.db_config_local import *

def run_record(record_name):

    #print('Record Name: ', record_name)
    ecg = ECG(data=LOCAL_DB, name=None, record=record_name)
    ecg._cwt_filtration()
    ecg._save_local(ECGDataDetails.filtrated)
    ecg._dwt()
    ecg._save_local(ECGDataDetails.wdc)
    ecg._delineation()
    ecg._adaptive_filtration()
    ecg._del_correction()
    ecg._characteristics()
    ecg._init_plot_data()

    ecg._save_local(ECGDataDetails.qrs_delineation)
    ecg._save_local(ECGDataDetails.qrs_morphology)

    ecg._save_local(ECGDataDetails.t_delineation)
    ecg._save_local(ECGDataDetails.t_morphology)

    ecg._save_local(ECGDataDetails.p_delineation)
    ecg._save_local(ECGDataDetails.p_morphology)

    ecg._save_local(ECGDataDetails.flutter_delineation)

    ecg._save_local(ECGDataDetails.adaptive_filtrated)

    ecg._save_local(ECGDataDetails.characteristics)

    ecg._save_local(ECGDataDetails.qrs_plot_data)