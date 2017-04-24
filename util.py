import enum

class Party(enum.Enum):
    DEM = 'democrat'
    GOP = 'republican'
    OTHER = 'Independent'

    def __str__(self):
        if (self == Party.DEM): return 'D'
        if (self == Party.GOP): return 'R'
        return 'I'

def party_str(pstr):
    if pstr.strip() in ['republican', 'Republican', 'rep', 'GOP', 'R', 'r']:
        return Party['GOP']
    elif pstr.strip() in ['democrat', 'Democrat', 'dem', 'DEM', 'D', 'd']:
        return Party['DEM']
    else:
        return Party['OTHER']
