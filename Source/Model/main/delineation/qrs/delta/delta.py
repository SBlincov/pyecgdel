from Source.Model.main.delineation.qrs.delta.matrix import *
from Source.Model.main.delineation.qrs.delta.addition import *
from Source.Model.main.delineation.qrs.delta.removal import *
from Source.Model.main.delineation.qrs.delta.shift import *
from Source.Model.main.zero_crossings.routines import *
from Source.Model.main.threshold_crossings.routines import *


def qrs_multi_lead_processing(leads):
    num_leads = len(leads)

    del_data = DelData(leads)
    integral_data = IntegralData(leads, del_data)

    shift_all(leads, del_data, integral_data)

    for del_id in range(0, integral_data.num_dels):

        count = integral_data.counts[del_id]
        ons = integral_data.ons[del_id]
        offs = integral_data.offs[del_id]

        if count > 0:
            mean_ons = int(np.mean(ons))
            mean_offs = int(np.mean(offs))

            # Check for removing
            if count <= int(QRSParams['DELTA_MAX_QRS_LOST'] * num_leads):
                remove_complex(leads, integral_data.mtx, del_id)

            # Check for adding
            if count >= int(QRSParams['DELTA_MIN_QRS_FOUND'] * num_leads):
                add_complex(leads, integral_data.mtx, del_id, mean_ons, mean_offs)

    restore_morph_order(leads)
    delete_nearest(leads)
    restore_morph_order(leads)






