from Source.Model.main.ecg.ecg import *
from Source.CardioBase.cardiobase import Cardiobase

id_file = 1007

cb = Cardiobase()
cb.connect()

params_hash = cb.get_hash(656)

config_params_from_hash = params_hash['data'][0]
p_params_from_hash = params_hash['data'][1]
qrs_params_from_hash = params_hash['data'][2]
t_params_from_hash = params_hash['data'][3]
filter_params_from_hash = params_hash['data'][4]

leads_names = ConfigParams['LEADS_NAMES']
