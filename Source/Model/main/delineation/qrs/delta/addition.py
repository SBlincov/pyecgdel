from Source.Model.main.delineation.qrs.gamma.gamma import *
from Source.Model.main.delineation.qrs.delta.removal import *


def add_complex(leads, corr_mtx, g_id, mean_qrs_on, mean_qrs_off):

    qrs_del_extra = WaveDelineation()
    qrs_del_extra.onset_index = mean_qrs_on
    qrs_del_extra.offset_index = mean_qrs_off
    qrs_del_extra.specification = WaveSpecification.exist

    num_leads = len(leads)

    for lead_id in range(0, num_leads):

        # Add only in missed leads
        if corr_mtx[lead_id][g_id] == -1:

            lead = leads[lead_id]

            # Search ZCSs in averaged interval
            qrs_del_extra_zcs = get_zcs_in_window(lead.zcs[int(QRSParams['WDC_SCALE_ID'])],
                                                        qrs_del_extra.onset_index,
                                                        qrs_del_extra.offset_index)

            # If ZCSs exist in averaged interval
            if qrs_del_extra_zcs:

                # Search ZCS with maximum mm_amplitude
                qrs_del_extra_zc = qrs_del_extra_zcs[0]
                for zc_id in range(1, len(qrs_del_extra_zcs)):
                    if qrs_del_extra_zcs[zc_id].g_ampl > qrs_del_extra_zc.g_ampl:
                        qrs_del_extra_zc = qrs_del_extra_zcs[zc_id]

                qrs_del_extra.peak_index = qrs_del_extra_zc.index
                qrs_del_id = 0

                if not lead.qrs_dels: # If there is no QRS complexes
                    lead.qrs_dels.append(qrs_del_extra)
                elif qrs_del_extra.peak_index < lead.qrs_dels[0].peak_index: # If found QRS is first
                    lead.qrs_dels.insert(qrs_del_id, qrs_del_extra)
                elif qrs_del_extra.peak_index > lead.qrs_dels[-1].peak_index: # If found QRS is last
                    qrs_del_id = len(lead.qrs_dels)
                    lead.qrs_dels.append(qrs_del_extra)
                else: # Search middle position for new QRS
                    for del_id in range(1, len(lead.qrs_dels)):
                        if lead.qrs_dels[del_id - 1].peak_index < qrs_del_extra.peak_index < \
                                lead.qrs_dels[del_id].peak_index:
                            qrs_del_id = del_id
                            lead.qrs_dels.insert(qrs_del_id, qrs_del_extra)

                # Init morphology for new QRS
                morphology = get_qrs_morphology(lead, qrs_del_id, lead.qrs_dels[qrs_del_id])
                # We should not change del_id in morphology of new QRS
                morphology.del_id = -1
                # Add morphology with mock del_id
                lead.qrs_morphs.insert(qrs_del_id, morphology)

                qrs_del_extra.onset_index = mean_qrs_on
                qrs_del_extra.offset_index = mean_qrs_off
