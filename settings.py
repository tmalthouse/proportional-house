from util import *

VOTE_THRESHOLD = 0.05

YEAR_DATA = {2012: {'pres': 'data/pres_2012.csv',
                 'house': 'data/house_2012.csv',
                 'results': {Party.GOP: 0.472, Party.DEM: 0.511}},
         2016: {'pres': 'data/pres_2016.csv',
                          'house': 'data/house_2016.csv',
                          'results': {Party.GOP: 0.461, Party.DEM: 0.482}}}
