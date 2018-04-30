from Source.Model.main.characteristics.characteristics_names import *

def get_flutter_chars(lead):
    flutter_chars = []

    flutter_chars.append([CharacteristicsNames.flutter, float(lead.flutter)])

    return flutter_chars