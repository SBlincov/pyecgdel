from Source.Model.main.delineation.p.routines import get_p_wdc_scale_id
from Source.Model.main.delineation.t.beta.data import TMorphologyData
from Source.Model.main.params.t import TParams
from Source.Model.main.delineation.wave_delineation import *
from Source.Model.main.delineation.t.beta.points import *


def get_t_morphology(ecg_lead, del_id, delineation):

    main_scale_id = get_p_wdc_scale_id(ecg_lead)
    aux_scale_id = int(TParams['BETA_SCALE'])

    p_morphology_data_main = TMorphologyData(ecg_lead, delineation, main_scale_id)
    p_morphology_data_aux = TMorphologyData(ecg_lead, delineation, aux_scale_id)

    if hasattr(p_morphology_data_main, 'zcs'):
        num_zcs_main = len(p_morphology_data_main.zcs)
    else:
        num_zcs_main = 0

    degree = Degree.unknown

    # In the case of adequate data
    if p_morphology_data_aux.correct == 1:

        zcs = p_morphology_data_aux.zcs
        t_zc_id = p_morphology_data_aux.peak_zc_id

        # Check: how many big zcs in delineation
        zc_ampl_th = zcs[t_zc_id].mm_amplitude * float(TParams['BETA_PEAK_ZC_AMPL'])
        big_zcs_ids = []
        for zc_id in range(0, len(zcs)):
            if zcs[zc_id].mm_amplitude > zc_ampl_th:
                big_zcs_ids.append(zc_id)

        num_big_zcs = len(big_zcs_ids)

        # Checking degree
        if num_zcs_main > 2:
            degree = Degree.unknown
        else:
            if num_big_zcs == num_zcs_main:
                degree = Degree.satisfyingly
            elif num_big_zcs == num_zcs_main + 1:
                degree = Degree.doubtfully
            else:
                degree = Degree.unknown

        # Getting points
        points = points_processing(ecg_lead, delineation, p_morphology_data_aux)

    else:
        # Getting points
        if p_morphology_data_main.correct:
            points = points_processing(ecg_lead, delineation, p_morphology_data_main)
        else:
            points = points_processing_trivial(ecg_lead, delineation)

    branch_id = [0, 0]

    morphology = Morphology(del_id, points, degree, branch_id)

    return morphology

