from Source.Model.main.delineation.qrs.gamma.gamma import *
from Source.Model.main.delineation.qrs.delta.removal import *


def add_complex(leads, corr_mtx, count_id, qrs_del_extra, del_candidates):

    num_leads = len(leads)
    mean_qrs_on = qrs_del_extra.onset_index
    mean_qrs_off = qrs_del_extra.offset_index

    for lead_id in range(0, num_leads):

        if corr_mtx[lead_id][count_id] == -1:
            lead = leads[lead_id]

            if [lead_id, count_id] in del_candidates:

                remove_del_candidate(lead, corr_mtx, lead_id, count_id)

            qrs_del_extra_zcs = get_zcs_with_global_mms(lead.wdc[int(QRSParams['WDC_SCALE_ID'])],
                                                        qrs_del_extra.onset_index,
                                                        qrs_del_extra.offset_index)

            if qrs_del_extra_zcs:

                qrs_del_extra_zc = qrs_del_extra_zcs[0]
                for zc_id in range(1, len(qrs_del_extra_zcs)):
                    if qrs_del_extra_zcs[zc_id].mm_amplitude > qrs_del_extra_zc.mm_amplitude:
                        qrs_del_extra_zc = qrs_del_extra_zcs[zc_id]

                qrs_del_extra.peak_index = qrs_del_extra_zc.index
                qrs_del_id = 0

                if not lead.qrs_dels:
                    lead.qrs_dels.append(qrs_del_extra)
                elif qrs_del_extra.peak_index < lead.qrs_dels[0].peak_index:
                    lead.qrs_dels.insert(qrs_del_id, qrs_del_extra)
                elif qrs_del_extra.peak_index > lead.qrs_dels[-1].peak_index:
                    qrs_del_id = len(lead.qrs_dels)
                    lead.qrs_dels.append(qrs_del_extra)
                else:
                    for del_id in range(1, len(lead.qrs_dels)):
                        if lead.qrs_dels[del_id - 1].peak_index < qrs_del_extra.peak_index < \
                                lead.qrs_dels[del_id].peak_index:
                            qrs_del_id = del_id
                            lead.qrs_dels.insert(qrs_del_id, qrs_del_extra)

                morphology = get_qrs_morphology(lead, qrs_del_id, lead.qrs_dels[qrs_del_id])
                lead.qrs_morphs.insert(qrs_del_id, morphology)
                qrs_del_extra.onset_index = mean_qrs_on
                qrs_del_extra.offset_index = mean_qrs_off
