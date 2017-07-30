class QRSDefaultParams:

    WDC_SCALE_ID = 2
    WDC_SCALE_ID_AUX = 3

    CANDIDATE_WINDOW_MIN_BEAT = 0.280
    CANDIDATE_WINDOW_TRAINING_PERIOD = 8.0
    CANDIDATE_BEATS_COUNT_TRAINING_PERIOD = 4
    CANDIDATE_WINDOW_DELTA = 0.100
    CANDIDATE_THRESHOLD_DELTA = 0.5

    ONSET_WINDOW = 0.100
    ONSET_THRESHOLD_MM = 0.07
    ONSET_AMPLITUDE_DECREASING = 0.7
    ONSET_AMPLITUDE_DECREASING_POW = 4
    ONSET_THRESHOLD = 0.25
    ONSET_MM_VALUE_COEFF = 0.5
    ONSET_MM_INDEX_SHIFT = 0.06
    ONSET_COMPROMISE_WINDOW = 0.055
    ONSET_COMPROMISE_MM_VALUE_COEFF = 0.5

    WIDE_ZC_AMPLITUDE_COEFF = 0.3
    WIDE_MM_VALUE_COEFF = 0.6

    OFFSET_WINDOW = 0.150
    OFFSET_THRESHOLD_MM = 0.09
    OFFSET_THRESHOLD = 0.3

    EXTRA_BEAT_PART = 0.7

    MUTABILITY_PERCENTAGE = 0.3

    MORPHOLOGY_NORMAL = 0.13
    MORPHOLOGY_ALLOWED_DIFF_PART_LEFT = 0.8
    MORPHOLOGY_ALLOWED_DIFF_PART_RIGHT = 0.8
    MORPHOLOGY_MM_SMALL_PART_LEFT = 0.001
    MORPHOLOGY_MM_SMALL_PART_RIGHT = 0.001
    MORPHOLOGY_R_NEG_PART = 0.85
    MORPHOLOGY_SCALES_DIFF = 2.0
    MORPHOLOGY_WINDOW_INCREASE = 0.013
    MORPHOLOGY_OFFSET_INCORRECT_COEFF = 5
    MORPHOLOGY_ONSET_TH = 0.25
    MORPHOLOGY_OFFSET_TH = 0.25
    MORPHOLOGY_M_AMPLITUDE_PART = 0.7

    GAMMA_LEFT_ODD_XTD_ZCS_SHIFT = 0.03
    GAMMA_RIGHT_ODD_XTD_ZCS_SHIFT = 0.03
    GAMMA_LEFT_EVEN_XTD_ZCS_SHIFT = 0.014
    GAMMA_RIGHT_EVEN_XTD_ZCS_SHIFT = 0.014
    GAMMA_LEFT_XTD_ZCS_MM_PART = 0.2
    GAMMA_RIGHT_XTD_ZCS_MM_PART = 0.2
    GAMMA_LEFT_WINDOW = 0.03
    GAMMA_RIGHT_WINDOW = 0.03
    GAMMA_LEFT_Q_PART = 0.7
    GAMMA_RIGHT_S_PART = 0.7
    GAMMA_LEFT_ORIGIN_INCORRECT = 0.005
    GAMMA_RIGHT_ORIGIN_INCORRECT = 0.005
    GAMMA_BORD_SCALE = 2


