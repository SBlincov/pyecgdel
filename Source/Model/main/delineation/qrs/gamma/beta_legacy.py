from Source.Model.main.params.qrs import *


def origin_scale_analysis(ecg_lead, morph_data):

    # Init data for original wdc scale
    scale_id_origin = int(QRSParams['WDC_SCALE_ID'])
    wdc_origin = morph_data.wdc[scale_id_origin]
    zcs_origin = morph_data.zcs[scale_id_origin]
    peak_zc_id_origin = morph_data.peak_zcs_ids[scale_id_origin]
    dels_zcs_ids_origin = morph_data.dels_zcs_ids[scale_id_origin]

    # Init zcs, which correspond to begin and end
    del_begin_zc_id_origin = dels_zcs_ids_origin[0]
    del_end_zc_id_origin = dels_zcs_ids_origin[-1]

    # Defining zcs, which correspond to begin and end:
    # Leave only one first zc on each side
    if del_begin_zc_id_origin <= peak_zc_id_origin <= del_end_zc_id_origin:

        begin_zc_id = peak_zc_id_origin
        if begin_zc_id > del_begin_zc_id_origin:
            begin_zc_id = begin_zc_id - 1

        end_zc_id = peak_zc_id_origin
        if end_zc_id < del_end_zc_id_origin:
            end_zc_id = end_zc_id + 1

        # Don't forget about shift:
        # del_begin_zc_id_origin is not necessary to be 0
        begin_zc_id = begin_zc_id - del_begin_zc_id_origin
        end_zc_id = end_zc_id - del_begin_zc_id_origin

        dels_zcs_ids_origin = dels_zcs_ids_origin[begin_zc_id:end_zc_id + 1]

    return dels_zcs_ids_origin
