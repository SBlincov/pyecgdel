from Source.Model.main.ecg.ecg import *
from Source.Infrastructure.main.db_config_local import *

def run_record(record_name):

    print('Record Name: ', record_name)
    ecg = ECG(data=LOCAL_DB, name=None, record=record_name)
    ecg.cwt_filtration()
    ecg.save_local(ECGDataDetails.filtrated)
    ecg.dwt()
    ecg.save_local(ECGDataDetails.wdc)
    ecg.delineation()
    ecg.adaptive_filtration()
    ecg.del_correction()
    ecg.characteristics()
    ecg.init_plot_data()

    ecg.save_local(ECGDataDetails.qrs_delineation)
    ecg.save_local(ECGDataDetails.qrs_morphology)

    ecg.save_local(ECGDataDetails.t_delineation)
    ecg.save_local(ECGDataDetails.t_morphology)

    ecg.save_local(ECGDataDetails.p_delineation)
    ecg.save_local(ECGDataDetails.p_morphology)

    ecg.save_local(ECGDataDetails.adaptive_filtrated)

    ecg.save_local(ECGDataDetails.characteristics)

    ecg.save_local(ECGDataDetails.qrs_plot_data)