from Source.Model.main.ecg.ecg import *
from Source.Model.main.plot_data.qrs import *

def set_record(record_name, cb, columns_names):

    print(record_name)

    d = {}
    local_path = DBConfig.get_db_path() + "\\" + record_name + "\\"

    file_id = int(record_name[7:])

    data = cb.bulk_data_get(columns_names, "cardio_file.id=" + str(file_id))
    if len(data['data']) != 0:
        for column_name in columns_names:
            cb.delete(file_id, column_name)

    if file_id != -1:
        print(': file_id: ', file_id)

        for lead in cb.leads:
            print(lead)

            filtrated = np.loadtxt(local_path + '/lead_' + lead + '/adaptive_filtrated.txt')
            d["json_lead_" + lead + "_filtrated"] = [(file_id, filtrated.tolist())]

            p_delineation = np.loadtxt(local_path + '/lead_' + lead + '/p_delineation.txt', dtype=np.int)
            print("p_del shape: ", p_delineation.shape)
            if len(p_delineation) == 0:
                d["json_lead_" + lead + "_p_delineation"] = [(file_id, [])]
            elif p_delineation.ndim == 1:
                d["json_lead_" + lead + "_p_delineation"] = [(file_id, [p_delineation.tolist()])]
            else:
                d["json_lead_" + lead + "_p_delineation"] = [(file_id, p_delineation.tolist())]

            qrs_delineation = np.loadtxt(local_path + '/lead_' + lead + '/qrs_delineation.txt', dtype=np.int)
            print("qrs_del shape: ", qrs_delineation.shape)
            if len(qrs_delineation) == 0:
                d["json_lead_" + lead + "_qrs_delineation"] = [(file_id, [])]
            elif qrs_delineation.ndim == 1:
                d["json_lead_" + lead + "_qrs_delineation"] = [(file_id, [qrs_delineation.tolist()])]
            else:
                d["json_lead_" + lead + "_qrs_delineation"] = [(file_id, qrs_delineation.tolist())]

            t_delineation = np.loadtxt(local_path + '/lead_' + lead + '/t_delineation.txt', dtype=np.int)
            print("t_del shape: ", t_delineation.shape)
            if len(t_delineation) == 0:
                d["json_lead_" + lead + "_t_delineation"] = [(file_id, [])]
            elif t_delineation.ndim == 1:
                d["json_lead_" + lead + "_t_delineation"] = [(file_id, [t_delineation.tolist()])]
            else:
                d["json_lead_" + lead + "_t_delineation"] = [(file_id, t_delineation.tolist())]

            print("\n")

            char_path = local_path + '/lead_' + lead + '/characteristics.txt'
            lines = [line.rstrip('\n') for line in open(char_path)]
            ch_names = []
            ch_values = []
            for line in lines:
                ch = line.split()
                ch_names.append(ch[0])
                if (ch[1]) != 'n':
                    ch_values.append(float(ch[1]))
                else:
                    ch_values.append(None)
            d["json_lead_" + lead + "_characteristics"] = [(file_id, [ch_names, ch_values])]

            p_morphs_path = local_path + '/lead_' + lead + '/p_morphology.txt'
            lines = [line.rstrip('\n') for line in open(p_morphs_path)]
            p_records = []
            for line in lines:
                p_m = line.split()
                p_records.append(p_m[0:6])

            d["json_lead_" + lead + "_p_morphology"] = [(file_id, p_records)]

            qrs_morphs_path = local_path + '/lead_' + lead + '/qrs_morphology.txt'
            lines = [line.rstrip('\n') for line in open(qrs_morphs_path)]
            qrs_records = []
            for line in lines:
                qrs_m = line.split()
                qrs_records.append(qrs_m[0:6])

            d["json_lead_" + lead + "_qrs_morphology"] = [(file_id, qrs_records)]

            t_morphs_path = local_path + '/lead_' + lead + '/t_morphology.txt'
            lines = [line.rstrip('\n') for line in open(t_morphs_path)]
            t_records = []
            for line in lines:
                t_m = line.split()
                t_records.append(t_m[0:6])

            d["json_lead_" + lead + "_t_morphology"] = [(file_id, t_records)]

            for plot_data_name in QRSPlotDataNames:
                plot_data_path = local_path + '/lead_' + lead + '/' + plot_data_name.value + '.txt'
                column_name = "json_lead_" + lead + "_" + plot_data_name.value
                plot_data = np.loadtxt(plot_data_path)
                d[column_name] = [(file_id, plot_data.tolist())]

        cb.bulk_data_set(d)
        cb.commit()
        print("\n")
        print("\n")


