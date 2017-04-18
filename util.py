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
    if pstr in ['republican', 'Republican', 'rep', 'GOP']:
        return Party['GOP']
    elif pstr in ['democrat', 'Democrat', 'dem', 'DEM']:
        return Party['DEM']
    else:
        return Party['OTHER']
