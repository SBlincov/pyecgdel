import numpy as np
from Source.Model.main.delineation.qrs.delta.data import *
from Source.Model.main.search.closest_position import *

def restore_morph_order(leads):
    num_leads = len(leads)
    for lead_id in range(0, num_leads):
        lead = leads[lead_id]
        for morph_id in range(0, len(lead.qrs_morphs)):
            lead.qrs_morphs[morph_id].del_id = morph_id

