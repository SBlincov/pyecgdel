from Source.Infrastructure.main.config import *
from Source.Model.main.params.flutter import *
from Source.Model.main.zero_crossings.routines import *
from Source.Model.main.delineation.wave_delineation import *
from Source.Model.main.threshold_crossings.routines import *


def flutter_analysis(leads):

    leads_names = FlutterParams['LEADS_NAMES']
    wdc_scale_id = int(FlutterParams['WDC_SCALE_ID'])
    zcs_min_num = int(FlutterParams['ZCS_MIN_NUM'])
    peaks_min_num = int(FlutterParams['PEAKS_MIN_NUM'])
    max_std_ampl = float(FlutterParams['MAX_STD_AMPL'])

    target_leads = [lead for lead in leads if lead.name in leads_names]

    for lead in target_leads:
        wdc = lead.wdc[wdc_scale_id]
        all_zcs = lead.zcs[wdc_scale_id]
        all_mms = lead.mms[wdc_scale_id]

        num_total_segments = len(lead.qrs_dels) - 1
        num_passed_segments = 0
        flutter_dels = []
        for seg_id in range(0, num_total_segments):
            begin_index = lead.qrs_dels[seg_id].offset_index
            end_index = lead.qrs_dels[seg_id + 1].onset_index

            zcs = get_zcs_in_window(lead.wdc[wdc_scale_id], lead.zcs[wdc_scale_id], begin_index, end_index)
            if len(zcs) > 0:

                # Special check for first zc
                if (abs(zcs[0].g_l_mm.value) > abs(zcs[0].g_r_mm.value)):
                    zcs.pop(0)

                if len(zcs) > 0:

                    # Special check for last zc
                    if (abs(zcs[-1].g_l_mm.value) < abs(zcs[-1].g_r_mm.value)):
                        zcs.pop()

                    if len(zcs) > zcs_min_num:

                        ampls = []

                        for zc_id in range(0, len(zcs)):
                            zc = zcs[zc_id]
                            ampls.append(zc.g_ampl)

                        mean = np.mean(np.asarray(ampls))
                        std = np.std(np.asarray(ampls))

                        zc_ids_to_delete = []

                        for zc_id in range(0, len(zcs)):
                            zc = zcs[zc_id]
                            if abs(zc.g_ampl - mean) > std * max_std_ampl:
                                zc_ids_to_delete.append(zc_id)

                        for zc_id in reversed(zc_ids_to_delete):
                            zcs.pop(zc_id)

                        target_zcs = [zc for zc in zcs if zc.g_r_mm.value > 0.0]

                        if len(target_zcs) > peaks_min_num:
                            num_passed_segments += 1
                            # Now we add flutter delineation
                            for zc in target_zcs:
                                flutter_del = WaveDelineation(WaveSpecification.exist)
                                onset_index = all_zcs[zc.id - 1].index - 1
                                offset_cand_1 = all_zcs[zc.id + 1].index
                                next_mm = all_mms[zc.r_mms[0].id]
                                offset_cand_2 = all_mms[next_mm.id + 1].index

                                offset_index = min(offset_cand_1, offset_cand_2)

                                flutter_del.peak_index = zc.index
                                flutter_del.onset_index = onset_index
                                flutter_del.offset_index = offset_index

                                flutter_dels.append(flutter_del)

        lead.flutter_dels = flutter_dels
        lead.flutter = float(num_passed_segments / num_total_segments)










