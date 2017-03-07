from Source.CardioBase.cardiobase import Cardiobase

id_file = 703

cb = Cardiobase()
cb.connect()
cb.cardio_event("SIGNALS", "PARSE_EDF_DONE", id_file)

cb.disconnect()

