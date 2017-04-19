import csv
from state import *
from representative import *
import util
import mapwriter

def main():
    with open("../election_2016_data/data/house_general_election_2016.csv", "r") as house:
        reader = csv.DictReader(house)
        states = dict()
        for row in reader:
            curState = row['state']
            if row['is_winner'] == 'True':
                try:
                    states[curState].delegation += 1
                except:
                    states[curState] = State(curState, 1)
                rep = Representative(row['name'], util.party_str(row['individual_party']))
                states[curState].reps.append(rep)




    with open("../election_2016_data/data/presidential_general_election_2016.csv") as pres:
        reader = csv.DictReader(pres)
        for row in reader:
            curState = row['state']
            if curState in states:
                states[curState].voteshare[util.party_str(row['individual_party'])] += float(row['vote_pct'])/100

    dem = 0
    rep = 0
    ind = 0
    for k in states:
        state=states[k]

        print(state)
        print("Pres. share:")
        for s in state.voteshare:
            print("{}: {:.1%}".format(s, state.voteshare[s]))

        state.calculate_prop()
        print("Rep. share:")

        print("D: {:.1%}".format(state.prop_rep[util.Party.DEM]/(state.delegation*2)))

        print("R: {:.1%}".format(state.prop_rep[util.Party.GOP]/(state.delegation*2)))

        print("I: {:.1%}".format(state.prop_rep[util.Party.OTHER]/(state.delegation*2)))
        print(state.prop_rep)

        dem += state.prop_rep[util.Party.DEM]
        rep += state.prop_rep[util.Party.GOP]
        ind += state.prop_rep[util.Party.OTHER]

        print(state.check_prop())
    print("Total seats: D: {}, R: {}, I: {}".format(dem,rep,ind))

    old_colors = {}
    prop_colors = {}
    for s in states:
        state = states[s]
        old_colors[s] = mapwriter.lean_to_color({p: state.rep_share(p) for p in list(util.Party)},
                                                state.voteshare, state.delegation)

        prop_colors[s] = mapwriter.lean_to_color({p: state.prop_rep[p]/(2*state.delegation) for p in list(util.Party)}, state.voteshare, state.delegation*2)

    oldmap = mapwriter.MapWriter(old_colors)
    oldmap.generate()
    oldmap.write("old_map.svg")
    prop_map = mapwriter.MapWriter(prop_colors)
    prop_map.generate()
    prop_map.write("prop_map.svg")


if __name__=="__main__":
    main()
