from Source.Model.main.zero_crossings.routines import *
from Source.Model.main.delineation.p.gamma.gamma import *
from Source.Model.main.delineation.p.delta.removal import *


def add_complex(leads, corr_mtx, g_id, mean_p_on, mean_p_off):

    num_leads = len(leads)

    for lead_id in range(0, num_leads):

        # Add only in missed leads
        if corr_mtx[lead_id][g_id] == -1:

            lead = leads[lead_id]

            if len(lead.qrs_dels) > g_id:

                p_del_extra = WaveDelineation()
                p_del_extra.onset_index = mean_p_on
                p_del_extra.offset_index = mean_p_off
                p_del_extra.specification = WaveSpecification.exist



                # Check for allowed borders
                # First check offset and qrs border
                qrs_id = g_id
                while p_del_extra.offset_index > lead.qrs_dels[qrs_id].offset_index:
                    if qrs_id + 1 > len(lead.qrs_dels) - 1:
                        break
                    else:
                        qrs_id += 1

                if p_del_extra.offset_index > lead.qrs_dels[qrs_id].onset_index:
                    p_del_extra.offset_index = lead.qrs_dels[qrs_id].onset_index

                # First check onset and t border
                t_id = g_id
                is_t_id_dec = False
                if t_id < len(lead.t_dels):
                    while p_del_extra.onset_index > lead.t_dels[t_id].onset_index:
                        is_t_id_dec = True
                        if t_id + 1> len(lead.t_dels) - 1:
                            break
                        else:
                            t_id += 1
                    if is_t_id_dec == True:
                        t_id -= 1

                if t_id < len(lead.t_dels):
                    if p_del_extra.onset_index < lead.t_dels[t_id].offset_index:
                        p_del_extra.onset_index = lead.t_dels[t_id].offset_index

                p_on = p_del_extra.onset_index
                p_off = p_del_extra.offset_index

                # Search ZCSs in averaged interval
                p_del_extra_zcs = get_zcs_with_global_mms(lead.wdc[int(PParams['WDC_SCALE_ID'])],
                                                            p_del_extra.onset_index,
                                                            p_del_extra.offset_index)

                # If ZCSs exist in averaged interval
                if p_del_extra_zcs:

                    # Search ZCS with maximum mm_amplitude
                    p_del_extra_zc = p_del_extra_zcs[0]
                    for zc_id in range(1, len(p_del_extra_zcs)):
                        if p_del_extra_zcs[zc_id].mm_amplitude > p_del_extra_zc.mm_amplitude:
                            p_del_extra_zc = p_del_extra_zcs[zc_id]

                    p_del_extra.peak_index = p_del_extra_zc.index
                    p_del_id = 0

                    if not lead.p_dels: # If there is no P complexes
                        lead.p_dels.append(p_del_extra)
                    elif p_del_extra.peak_index < lead.p_dels[0].peak_index: # If found P is first
                        lead.p_dels.insert(p_del_id, p_del_extra)
                    elif p_del_extra.peak_index > lead.p_dels[-1].peak_index: # If found p is last
                        p_del_id = len(lead.p_dels)
                        lead.p_dels.append(p_del_extra)
                    else: # Search middle position for new P
                        for del_id in range(1, len(lead.p_dels)):
                            if lead.p_dels[del_id - 1].peak_index < p_del_extra.peak_index < \
                                    lead.p_dels[del_id].peak_index:
                                p_del_id = del_id
                                lead.p_dels.insert(p_del_id, p_del_extra)

                    # Init morphology for new P
                    morphology = get_p_morph(lead, p_del_id, lead.p_dels[p_del_id])
                    # We should not change del_id in morphology of new P
                    morphology.del_id = -1
                    # Add morphology with mock del_id
                    lead.p_morphs.insert(p_del_id, morphology)

                    p_del_extra.onset_index = p_on
                    p_del_extra.offset_index = p_off
