class QRSDefaultParams:

    WDC_SCALE_ID = 2
    WDC_SCALE_ID_AUX = 3

    ALPHA_MIN_BEAT = 0.280
    ALPHA_TRAINING_WINDOW = 8.0
    ALPHA_BEATS_IN_TRAINING_WINDOW = 4
    ALPHA_QRS_WINDOW = 0.100
    ALPHA_THRESHOLD = 0.5

    BETA_ONSET_WINDOW = 0.100
    BETA_ONSET_MM_LOW_LIM = 0.055
    BETA_ONSET_AMPL_DECR_VAL = 0.3
    BETA_ONSET_AMPL_DECR_POW = 4
    BETA_ONSET_THRESHOLD = 0.25
    BETA_ONSET_MM_HIGH_LIM = 0.5
    BETA_ONSET_MM_WINDOW = 0.06
    BETA_ONSET_COMPROMISE_WINDOW = 0.055
    BETA_ONSET_COMPROMISE_MM_LIM = 0.5
    BETA_OFFSET_WINDOW = 0.150
    BETA_OFFSET_MM_LOW_LIM = 0.075
    BETA_OFFSET_THRESHOLD = 0.09
    BETA_COMPLEX_ZC_AMPL = 0.3
    BETA_COMPLEX_MM_VAL = 0.6

    GAMMA_NORMAL_LENGTH = 0.13
    GAMMA_ALLOWED_DIFF_PART_LEFT = 0.8
    GAMMA_ALLOWED_DIFF_PART_RIGHT = 0.8
    GAMMA_R_NEG_PART = 0.85
    GAMMA_MM_SMALL_PART_LEFT = 0.001
    GAMMA_MM_SMALL_PART_RIGHT = 0.001
    GAMMA_SCALES_DIFF = 2.0
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

    EXTRA_BEAT_PART = 0.7
    MUTABILITY_PERCENTAGE = 0.3



