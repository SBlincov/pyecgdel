import numpy as np
from Source.Model.main.params.p import PParams
from Source.Model.main.delineation.wave_delineation import WaveSpecification

def check_for_atrial_fibrillation(delineation, zcs):

    zcs_amplitudes = []
    for zc in zcs:
        zcs_amplitudes.append(zc.mm_amplitude)

    zcs_amplitudes = np.asarray(zcs_amplitudes)

    if len(zcs) > int(PParams['LEGACY_FIB_NUM_ZCS']):

        zcs_amplitudes = np.sort(zcs_amplitudes)[::-1]
        zcs_amplitudes = zcs_amplitudes[1:int(PParams['LEGACY_FIB_NUM_ZCS']) + 1]

        zcs_amplitudes_mean = np.mean(zcs_amplitudes)
        zcs_amplitudes_std = np.std(zcs_amplitudes)

        if zcs_amplitudes_std < zcs_amplitudes_mean * float(PParams['LEGACY_FIB_STD']):
            delineation.specification = WaveSpecification.atrial_fibrillation