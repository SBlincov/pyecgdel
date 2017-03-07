# -*- coding: utf-8 -*-


import os

import numpy as np

from Source.CardioBase.cardiobase import Cardiobase

cb = Cardiobase()
cb.connect()
col = cb.get_columns()


patients = np.loadtxt('C:/Study/CyberHeart/trunk/diagnostics/database/ptbdb/patients.txt', dtype=np.int64)
path = 'C:/Study/CyberHeart/trunk/diagnostics/database/ptbdb/patient_'


for i in range(1, 1):
    for x in os.listdir(path+str(i)):      
        d = {}
        rec_path = path + str(i) + '/' + x
        id_file = cb.create_file(int(patients[i-1]), str(patients[i-1]) +  '_' + x)
        cb.close_file(id_file)

        for lead in cb.leads:

            original = np.loadtxt(rec_path + '/lead_' + lead +'/original.txt')
            filtrated = np.loadtxt(rec_path + '/lead_' + lead +'/filtrated.txt')
            p_delineation = np.loadtxt(rec_path + '/lead_' + lead +'/p_delineation.txt', dtype=np.int)
            qrs_delineation = np.loadtxt(rec_path + '/lead_' + lead +'/qrs_delineation.txt', dtype=np.int)
            t_delineation = np.loadtxt(rec_path + '/lead_' + lead +'/t_delineation.txt', dtype=np.int)
            d["lead_"+lead+"_original"] = [(id_file, original)]
            d["lead_"+lead+"_filtrated"] = [(id_file, filtrated)]
            d["lead_"+lead+"_p_delineation"] = [(id_file, p_delineation)]
            d["lead_"+lead+"_qrs_delineation"] = [(id_file, qrs_delineation)]
            d["lead_"+lead+"_t_delineation"] = [(id_file, t_delineation)]

            char_path = rec_path + '/lead_' + lead + '/characteristics.txt'
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
            d["lead_"+lead+"_characteristics"] = [(id_file, [ch_names, ch_values])]
        diag = np.genfromtxt(rec_path + '/diagnosis.txt', dtype='str', delimiter='\n')
        d["diagnosis"] = [(id_file, str(diag))]
        d["sampling_rate"] = [(id_file, 250.0)]
        
        cb.bulk_data_set(d)
        cb.commit()


#res = cb.bulk_data_get(list(col.keys()))
#res = cb.bulk_data_get(["diagnosis", "sampling_rate"])


cb.disconnect()


