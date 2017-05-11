import util
from operator import itemgetter
from settings import *

class State(object):
    def __init__(self, name, rep_count):
        self.name = name
        self.delegation = rep_count
        self.voteshare = {util.Party.DEM:0, util.Party.GOP:0, util.Party.OTHER:0}
        self.reps = list()
        self.prop_rep = {}

    def __contains__(self, state):
        return self.name == state

    def __eq__(self, state): return __contains__(self, state)

    def __str__(self):
        return self.name + ": " + str(self.delegation)

    def rep_share(self, party):
        rep_weight = 1/self.delegation
        share = 0
        for r in self.reps:
            if r.party == party:
                share += rep_weight
        return share

    def rep_shares(self):
        return {p: self.rep_share(p) for p in list(util.Party)}

    def party_count(self, party):
        tot = 0
        for r in self.reps:
            if r.party == party:
                tot+=1
        return tot

    def calculate_prop(self):
        total_delegation = 2*self.delegation

        current_seats = {util.Party.DEM:0, util.Party.GOP:0, util.Party.OTHER:0}
        for r in self.reps:
            current_seats[r.party] += 1

        while (sum(current_seats.values()) < total_delegation):
            quots = {}
            for p in list(util.Party):
                quots[p] = self.voteshare[p]/(2*current_seats[p]+1)

            # Give one seat to the party with the largest vote-share
            current_seats[max(quots.keys(), key=(lambda key: quots[key]))] += 1

        self.prop_rep = current_seats






    def check_prop(self):
        rep_total = self.delegation
        for party in list(util.Party):
            rep_total += self.prop_rep[party]
        return (rep_total/(self.delegation*2))
