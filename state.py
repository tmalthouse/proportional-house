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

    def party_count(self, party):
        tot = 0
        for r in self.reps:
            if r.party == party:
                tot+=1
        return tot

    def calculate_prop(self):
        total_delegation = 2*self.delegation
        self.prop_rep = {party: self.party_count(party) for party in list(util.Party)}
        total = sum(self.prop_rep.values())

        entries = []
        for n in range(1,self.delegation):
            for p in list(util.Party):
                if (self.voteshare[p]>VOTE_THRESHOLD):
                    entries.append(((self.voteshare[p]*(1/n))/(self.prop_rep[p]+n), p))

        entries.sort(key=itemgetter(0), reverse=True)


        for i in entries:
            party = i[1]
            self.prop_rep[party] += 1

            total = sum(self.prop_rep.values())
            if (total>=total_delegation): break


    def check_prop(self):
        rep_total = self.delegation
        for party in list(util.Party):
            rep_total += self.prop_rep[party]
        return (rep_total/(self.delegation*2))
