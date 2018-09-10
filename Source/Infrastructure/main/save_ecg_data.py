from .db_config_local import *
from .ecg_data_routines import *
from ...Model.main.data_details.ecg_data_details import *
from ...Model.main.ecg_lead.ecg_lead import *
from ...Model.main.ecg.ecg import *
from ...Model.main.params.common import *
import numpy as np
import os


def save_data_local(ecg, details):
    rate = float(ConfigParams['SAMPLING_RATE'])
    leads_names = ConfigParams['LEADS_NAMES']

    if abs(ecg.leads[0].rate - rate) > EPSILON:
        raise InvalidECGData('Sampling rate in current instance must be equal to sampling rate in database')

    for lead_id in range(len(leads_names)):

        test_file_name = DBConfig.get_db_lead_path(ecg._name, ecg._record, leads_names[lead_id], ECGDataDetails.original)
        data_file_name = DBConfig.get_db_lead_path(ecg._name, ecg._record, leads_names[lead_id], details)

        if os.path.exists(test_file_name):

            if ecg.leads[lead_id].name not in leads_names:
                raise InvalidECGData('ECG lead names must be agree with database')

            if details is ECGDataDetails.filtrated:
                np.savetxt(data_file_name, ecg.leads[lead_id].filter, fmt='%.3e')

            elif details is ECGDataDetails.adaptive_filtrated:
                np.savetxt(data_file_name, ecg.leads[lead_id].filter, fmt='%.3e')

            elif details is ECGDataDetails.wdc:
                np.savetxt(data_file_name, np.transpose(ecg.leads[lead_id].wdc), fmt='%.3e')

            elif details is ECGDataDetails.qrs_delineation:
                delineation_info = []
                for delineation in ecg.leads[lead_id].qrs_dels:
                    delineation_info.append([delineation.onset_index,
                                             delineation.peak_index,
                                             delineation.offset_index,
                                             delineation.specification.value])

                np.savetxt(data_file_name, delineation_info, fmt='%d')

            elif details is ECGDataDetails.qrs_morphology:

                del_ids = []
                names = []
                indexes = []
                values = []
                signs = []
                degrees = []
                branch_ids_0 = []
                branch_ids_1 = []

                for morph in ecg.leads[lead_id].qrs_morphs:

                    del_id = morph.del_id
                    branch_id = morph.branch_id
                    degree_id = morph.degree

                    for point in morph.points:
                        name = str(point.name)
                        index = point.index
                        value = point.value
                        sign = int(point.sign)
                        degree = int(degree_id)

                        del_ids.append(del_id)
                        names.append(name)
                        indexes.append(index)
                        values.append(value)
                        signs.append(sign)
                        degrees.append(degree)
                        branch_ids_0.append(branch_id[0])
                        branch_ids_1.append(branch_id[1])

                morphology_info = np.zeros(len(del_ids),
                                           dtype=[('var1', int), ('var2', 'U50'), ('var3', int), ('var4', float),
                                                  ('var5', int), ('var6', int), ('var7', int), ('var8', int)])
                fmt = "%d %s %d %8e %d %d %d %d"

                morphology_info['var1'] = del_ids
                morphology_info['var2'] = names
                morphology_info['var3'] = indexes
                morphology_info['var4'] = values
                morphology_info['var5'] = signs
                morphology_info['var6'] = degrees
                morphology_info['var7'] = branch_ids_0
                morphology_info['var8'] = branch_ids_1

                np.savetxt(data_file_name, morphology_info, fmt=fmt)

            elif details is ECGDataDetails.t_delineation:
                delineation_info = []
                for delineation in ecg.leads[lead_id].t_dels:
                    delineation_info.append([delineation.onset_index,
                                             delineation.peak_index,
                                             delineation.offset_index,
                                             delineation.specification.value])

                np.savetxt(data_file_name, delineation_info, fmt='%d')

            elif details is ECGDataDetails.t_morphology:

                del_ids = []
                names = []
                indexes = []
                values = []
                signs = []
                degrees = []
                branch_ids_0 = []
                branch_ids_1 = []

                for morph in ecg.leads[lead_id].t_morphs:

                    del_id = morph.del_id
                    branch_id = morph.branch_id
                    degree_id = morph.degree

                    for point in morph.points:
                        name = str(point.name)
                        index = point.index
                        value = point.value
                        sign = int(point.sign)
                        degree = int(degree_id)

                        del_ids.append(del_id)
                        names.append(name)
                        indexes.append(index)
                        values.append(value)
                        signs.append(sign)
                        degrees.append(degree)
                        branch_ids_0.append(branch_id[0])
                        branch_ids_1.append(branch_id[1])

                morphology_info = np.zeros(len(del_ids),
                                           dtype=[('var1', int), ('var2', 'U50'), ('var3', int), ('var4', float),
                                                  ('var5', int), ('var6', int), ('var7', int), ('var8', int)])
                fmt = "%d %s %d %8e %d %d %d %d"

                morphology_info['var1'] = del_ids
                morphology_info['var2'] = names
                morphology_info['var3'] = indexes
                morphology_info['var4'] = values
                morphology_info['var5'] = signs
                morphology_info['var6'] = degrees
                morphology_info['var7'] = branch_ids_0
                morphology_info['var8'] = branch_ids_1

                np.savetxt(data_file_name, morphology_info, fmt=fmt)

            elif details is ECGDataDetails.p_delineation:
                delineation_info = []
                for delineation in ecg.leads[lead_id].p_dels:
                    delineation_info.append([delineation.onset_index,
                                             delineation.peak_index,
                                             delineation.offset_index,
                                             delineation.specification.value])

                np.savetxt(data_file_name, delineation_info, fmt='%d')

            elif details is ECGDataDetails.p_morphology:

                del_ids = []
                names = []
                indexes = []
                values = []
                signs = []
                degrees = []
                branch_ids_0 = []
                branch_ids_1 = []

                for morph in ecg.leads[lead_id].p_morphs:

                    del_id = morph.del_id
                    branch_id = morph.branch_id
                    degree_id = morph.degree

                    for point in morph.points:
                        name = str(point.name)
                        index = point.index
                        value = point.value
                        sign = int(point.sign)
                        degree = int(degree_id)

                        del_ids.append(del_id)
                        names.append(name)
                        indexes.append(index)
                        values.append(value)
                        signs.append(sign)
                        degrees.append(degree)
                        branch_ids_0.append(branch_id[0])
                        branch_ids_1.append(branch_id[1])

                morphology_info = np.zeros(len(del_ids),
                                           dtype=[('var1', int), ('var2', 'U50'), ('var3', int), ('var4', float),
                                                  ('var5', int), ('var6', int), ('var7', int), ('var8', int)])
                fmt = "%d %s %d %8e %d %d %d %d"

                morphology_info['var1'] = del_ids
                morphology_info['var2'] = names
                morphology_info['var3'] = indexes
                morphology_info['var4'] = values
                morphology_info['var5'] = signs
                morphology_info['var6'] = degrees
                morphology_info['var7'] = branch_ids_0
                morphology_info['var8'] = branch_ids_1

                np.savetxt(data_file_name, morphology_info, fmt=fmt)

            elif details is ECGDataDetails.flutter_delineation:
                delineation_info = []
                for delineation in ecg.leads[lead_id].flutter_dels:
                    delineation_info.append([delineation.onset_index,
                                             delineation.peak_index,
                                             delineation.offset_index,
                                             delineation.specification.value])

                np.savetxt(data_file_name, delineation_info, fmt='%d')

            elif details is ECGDataDetails.characteristics:
                characteristics = ecg.leads[lead_id].chars
                names = [item[0].name for item in characteristics]
                values = [item[1] for item in characteristics]

                characteristics_info = np.zeros(len(names), dtype=[('var1', 'U50'), ('var2', float)])
                fmt = "%s %18e"

                nan = "n"
                if nan in values:
                    characteristics_info = np.zeros(len(names), dtype=[('var1', 'U50'), ('var2', 'U50')])
                    fmt = "%s %s"

                characteristics_info['var1'] = names
                characteristics_info['var2'] = values

                np.savetxt(data_file_name, characteristics_info, fmt=fmt)

            elif details is ECGDataDetails.qrs_plot_data:

                for plot_data_key in ecg.leads[lead_id].qrs_plot_data.dict:
                    data_file_name = DBConfig.get_db_lead_path(ecg._name, ecg._record, leads_names[lead_id], plot_data_key)
                    np.savetxt(data_file_name, ecg.leads[lead_id].qrs_plot_data.dict[plot_data_key], fmt='%.3e')

            else:
                raise InvalidECGDataDetails('Error! Invalid ecg details')
