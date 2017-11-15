from Source.Model.main.delineation.qrs.delta.data import DelData, AllLeadsData
from Source.Model.main.delineation.qrs.delta.matrix import *
from Source.Model.main.delineation.qrs.delta.addition import *
from Source.Model.main.delineation.qrs.delta.removal import *
import warnings


def multi_lead_processing(leads):

    num_leads = len(leads)

    del_data = DelData(leads)

    all_leads_data = AllLeadsData(del_data)

    corr_mtx = get_com_matrix(del_data, all_leads_data)

    for g_id in range(0, len(borders_counts)):

        qrs_count = 0
        mean_qrs_on = 0
        mean_qrs_off = 0

        for lead_id in range(0, num_leads):

            if corr_mtx[lead_id][g_id] > -1:
                qrs_count += 1
                mean_qrs_on += del_data.ons[lead_id][corr_mtx[lead_id][g_id]]
                mean_qrs_off += del_data.offs[lead_id][corr_mtx[lead_id][g_id]]

        if qrs_count > 0:

            mean_qrs_on = int(mean_qrs_on / qrs_count)
            mean_qrs_off = int(mean_qrs_off / qrs_count)

            qrs_del_extra = WaveDelineation()
            qrs_del_extra.onset_index = mean_qrs_on
            qrs_del_extra.offset_index = mean_qrs_off
            qrs_del_extra.specification = WaveSpecification.exist

            if qrs_count >= int(QRSParams['DELTA_MIN_QRS_FOUND'] * num_leads):

                add_complex(leads, corr_mtx, g_id, qrs_del_extra, del_candidates)

            if qrs_count <= int(QRSParams['DELTA_MAX_QRS_LOST'] * num_leads):

                remove_complex(leads, corr_mtx, g_id, qrs_del_extra, del_candidates)

    restore_morph_order(leads)


def restore_morph_order(leads):

    num_leads = len(leads)
    for lead_id in range(0, num_leads):
        lead = leads[lead_id]
        for morph_id in range(0, len(lead.qrs_morphs)):
            lead.qrs_morphs[morph_id].del_id = morph_id
