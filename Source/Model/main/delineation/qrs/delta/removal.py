def remove_complex(leads, corr_mtx, count_id, qrs_del_extra, del_candidates):

    num_leads = len(leads)

    for lead_id in range(0, num_leads):

        if corr_mtx[lead_id][count_id] > -1:
            lead = leads[lead_id]

            if [lead_id, count_id] in del_candidates:

                i = -1
                index = -1
                while index == -1:
                    i += 1
                    index = corr_mtx[lead_id][count_id - i]

                lead.qrs_dels.pop(index + i)
                lead.qrs_morphs.pop(index + i)

            for morph_id in range(0, len(lead.qrs_morphs)):
                if lead.qrs_morphs[morph_id].del_id == corr_mtx[lead_id][count_id]:
                    lead.qrs_dels.pop(morph_id)
                    lead.qrs_morphs.pop(morph_id)
                    break
