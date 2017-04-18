class Representative(object):
    def __init__(self, name, party):
        self.name = name
        self.party = party

    def __str__(self):
        return self.name + ' (' + str(self.party) + ')'
