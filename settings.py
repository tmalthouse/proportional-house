from util import *

VOTE_THRESHOLD = 0.05

YEAR_DATA = {2012: {'pres': '../pres_2012.csv',
                 'house': '../house_2012.csv',
                 'results': {Party.GOP: 0.472, Party.DEM: 0.511}},
         2016: {'pres': '../election_2016_data/data/presidential_general_election_2016.csv',
                          'house': '../election_2016_data/data/house_general_election_2016.csv',
                          'results': {Party.GOP: 0.461, Party.DEM: 0.482}}}
