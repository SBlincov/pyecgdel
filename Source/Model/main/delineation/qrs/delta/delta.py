from Source.Model.main.delineation.qrs.delta.matrix import *
from Source.Model.main.delineation.qrs.gamma.gamma import *


def multi_lead_processing(leads):

    num_leads = len(leads)

    ons = []
    offs = []
    len_of_dels = []
    mean_qrs = []

    # Considering all leads:
    #   Taking all onset and offset indexes
    #   Saving number of dels for each lead
    #   Saving mean QRS length for each lead
    for lead_id in range(0, num_leads):

        lead = leads[lead_id]
        dels = lead.qrs_dels

        len_of_dels.append(len(dels))

        ons_lead = []
        offs_lead = []
        mean_qrs_curr = 0.0
        for del_id in range(0, len_of_dels[lead_id]):
            on_index_curr = dels[del_id].onset_index
            off_index_curr = dels[del_id].offset_index
            ons_lead.append(on_index_curr)
            offs_lead.append(off_index_curr)
            mean_qrs_curr += (off_index_curr - on_index_curr)
        mean_qrs_curr /= len(dels)

        ons.append(ons_lead)
        offs.append(offs_lead)
        mean_qrs.append(mean_qrs_curr)

    # Computing global mean QRS length
    mean_qrs_global = np.mean(np.asarray(mean_qrs))

    diff_corr = mean_qrs_global * float(QRSParams['DELTA_MEAN_QRS_DIFF_CORR'])
    loc = mean_qrs_global * float(QRSParams['DELTA_MEAN_QRS_LOC'])

    # Computing lead id with maximum number of dels
    max_dels_lead_id = np.argmax(np.asarray(len_of_dels))
    if max_dels_lead_id.size > 1:
        max_dels_lead_id = max_dels_lead_id[0]

    # Creating array with all complexes:
    #   sum of values
    #   occurrence rate

    ons_sum = []
    offs_sum = []

    for on_id in range(0, len(ons[max_dels_lead_id])):
        ons_sum.append(ons[max_dels_lead_id][on_id])

    for off_id in range(0, len(offs[max_dels_lead_id])):
        offs_sum.append(offs[max_dels_lead_id][off_id])

    borders_counts = []
    for bord_id in range(0, len(ons_sum)):
        borders_counts.append(1)

    for lead_id in range(0, num_leads):

        # For all leads except init lead
        if lead_id != max_dels_lead_id:

            ons_lead = ons[lead_id]
            offs_lead = offs[lead_id]

            for del_id in range(0, len_of_dels[lead_id]):

                curr_num_global = len(borders_counts)

                on_diffs = []
                off_diffs = []
                for g_del_id in range(0, curr_num_global):
                    on_diffs.append(ons_lead[del_id] - ons_sum[g_del_id] / borders_counts[g_del_id])
                    off_diffs.append(offs_lead[del_id] - offs_sum[g_del_id] / borders_counts[g_del_id])

                on_argmin = np.argmin(np.absolute(np.asarray(on_diffs)))
                if on_argmin.size > 1:
                    on_argmin = on_argmin[0]
                on_min = on_diffs[on_argmin]

                off_argmin = np.argmin(np.absolute(np.asarray(off_diffs)))
                if off_argmin.size > 1:
                    off_argmin = off_argmin[0]
                off_min = off_diffs[off_argmin]

                # Additional checking of argmins
                if abs(on_argmin - off_argmin) == 1:

                    on_diff_own = on_diffs[on_argmin]
                    on_diff_der = on_diffs[off_argmin]

                    off_diff_own = off_diffs[off_argmin]
                    off_diff_der = off_diffs[on_argmin]

                    on_diff_diff_abs = abs(abs(on_diff_own) - abs(on_diff_der))
                    off_diff_diff_abs = abs(abs(off_diff_own) - abs(off_diff_der))

                    if (on_diff_diff_abs < off_diff_diff_abs) and (on_diff_diff_abs < diff_corr):

                        on_argmin = off_argmin
                        on_min = on_diffs[on_argmin]

                    elif (off_diff_diff_abs < on_diff_diff_abs) and (off_diff_diff_abs < diff_corr):

                        off_argmin = on_argmin
                        off_min = off_diffs[off_argmin]

                    else:

                        total_min = min([abs(on_diff_own), abs(on_diff_der), abs(off_diff_own), abs(off_diff_der)])

                        if total_min == abs(on_diff_own) or total_min == abs(off_diff_own):

                            on_argmin = off_argmin
                            on_min = on_diffs[on_argmin]

                        else:

                            off_argmin = on_argmin
                            off_min = off_diffs[off_argmin]

                on_curr = ons_sum[on_argmin] / borders_counts[on_argmin] + on_diffs[on_argmin]
                off_curr = offs_sum[off_argmin] / borders_counts[off_argmin] + off_diffs[off_argmin]

                if on_argmin == off_argmin:

                    argmin = on_argmin

                    if (abs(on_min) < loc) or (abs(off_min) < loc):

                        ons_sum[argmin] += on_curr
                        offs_sum[argmin] += off_curr
                        borders_counts[argmin] += 1

                    else:

                        if (on_diffs[argmin] < 0.0) and (off_diffs[argmin] < 0.0):
                            ons_sum.insert(argmin, on_curr)
                            offs_sum.insert(argmin, off_curr)
                            borders_counts.insert(argmin, 1)
                        elif (on_diffs[argmin] > 0.0) and (off_diffs[argmin] > 0.0):
                            ons_sum.insert(argmin + 1, on_curr)
                            offs_sum.insert(argmin + 1, off_curr)
                            borders_counts.insert(argmin + 1, 1)
                        else:
                            raise Exception("Wrong left and right diffs")

                else:

                    raise Exception("Onset and offset out of correspondence")

    corr_mtx = get_com_matrix(leads, borders_counts, ons_sum, offs_sum)

    for count_id in range(0, len(borders_counts)):

        qrs_count = 0
        mean_qrs_on = 0
        mean_qrs_off = 0

        for lead_id in range(0, num_leads):

            if corr_mtx[lead_id][count_id] > -1:
                qrs_count += 1
                mean_qrs_on += ons[lead_id][corr_mtx[lead_id][count_id]]
                mean_qrs_off += offs[lead_id][corr_mtx[lead_id][count_id]]

        mean_qrs_on = int(mean_qrs_on / qrs_count)
        mean_qrs_off = int(mean_qrs_off / qrs_count)

        qrs_del_extra = WaveDelineation()
        qrs_del_extra.onset_index = mean_qrs_on
        qrs_del_extra.offset_index = mean_qrs_off
        qrs_del_extra.specification = WaveSpecification.exist

        if qrs_count >= int(QRSParams['DELTA_MIN_QRS_FOUND']):

            for lead_id in range(0, num_leads):

                if corr_mtx[lead_id][count_id] == -1:
                    lead = leads[lead_id]
                    qrs_del_extra_zcs = get_zcs_with_global_mms(lead.wdc[int(QRSParams['WDC_SCALE_ID'])],
                                                                qrs_del_extra.onset_index,
                                                                qrs_del_extra.offset_index)

                    qrs_del_extra_zc = qrs_del_extra_zcs[0]
                    for zc_id in range(1, len(qrs_del_extra_zcs)):
                        if qrs_del_extra_zcs[zc_id].mm_amplitude > qrs_del_extra_zc.mm_amplitude:
                            qrs_del_extra_zc = qrs_del_extra_zcs[zc_id]

                    qrs_del_extra.peak_index = qrs_del_extra_zc.index
                    qrs_del_id = 0

                    if qrs_del_extra.peak_index < lead.qrs_dels[0].peak_index:
                        lead.qrs_dels.insert(qrs_del_id, qrs_del_extra)
                    elif qrs_del_extra.peak_index > lead.qrs_dels[-1].peak_index:
                        qrs_del_id = len(lead.qrs_dels)
                        lead.qrs_dels.append(qrs_del_extra)
                    else:
                        for del_id in range(1, len(lead.qrs_dels)):
                            if lead.qrs_dels[del_id-1].peak_index < qrs_del_extra.peak_index < \
                                    lead.qrs_dels[del_id].peak_index:
                                qrs_del_id = del_id
                                lead.qrs_dels.insert(qrs_del_id, qrs_del_extra)

                    morphology = get_qrs_morphology(lead, qrs_del_id, lead.qrs_dels[qrs_del_id])
                    lead.qrs_morphs.insert(qrs_del_id, morphology)

        if qrs_count <= int(QRSParams['DELTA_MAX_QRS_LOST']):

            for lead_id in range(0, num_leads):

                if corr_mtx[lead_id][count_id] > -1:
                    lead = leads[lead_id]
                    for morph_id in range(0, len(lead.qrs_morphs)):
                        if lead.qrs_morphs[morph_id].del_id == corr_mtx[lead_id][count_id]:
                            lead.qrs_dels.pop(morph_id)
                            lead.qrs_morphs.pop(morph_id)
                            break

    for lead_id in range(0, num_leads):
        lead = leads[lead_id]
        for morph_id in range(0, len(lead.qrs_morphs)):
            lead.qrs_morphs[morph_id].del_id = morph_id
