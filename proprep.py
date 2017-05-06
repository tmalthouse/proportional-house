#! /usr/local/bin/python3

import csv
from state import *
from representative import *
import util
import mapwriter
import argparse
import latex
import os

def main():
    parser = argparse.ArgumentParser(description="Generate maps comparing the actual and theoretical proportional representation in a given year.")
    parser.add_argument('year', action='store', default='2016', type=int)
    parser.add_argument('--latex', dest='latex', action='store_true')

    args = parser.parse_args()
    year = args.year

    try:
        a = YEAR_DATA[year]
    except Exception as e:
        print("No data available for {}. Note that the analysis only works in presidential years.".format(year))
        return -1

    with open(YEAR_DATA[year]['house'], "r") as house:
        reader = csv.DictReader(house)
        states = dict()
        for row in reader:
            curState = row['state'].title().strip()
            if row['is_winner'].upper() == 'TRUE':
                try:
                    states[curState].delegation += 1
                except:
                    states[curState] = State(curState, 1)
                rep = Representative(row['name'], util.party_str(row['individual_party']))
                states[curState].reps.append(rep)




    with open(YEAR_DATA[year]['pres']) as pres:
        reader = csv.DictReader(pres)
        for row in reader:
            curState = row['state'].title().strip()
            if curState in states:
                states[curState].voteshare[util.party_str(row['individual_party'])] += float(row['vote_pct'])/100


    totals = {util.Party.DEM: 0, util.Party.GOP: 0, util.Party.OTHER: 0}
    for k in states:
        state=states[k]

        print(state)
        for r in state.reps:
            print(r)
        print("Pres. share:")
        for s in state.voteshare:
            print("{}: {:.1%}".format(s, state.voteshare[s]))

        state.calculate_prop()
        print("Rep. share:")

        print("D: {:.1%}".format(state.prop_rep[util.Party.DEM]/(state.delegation*2)))

        print("R: {:.1%}".format(state.prop_rep[util.Party.GOP]/(state.delegation*2)))

        print("I: {:.1%}".format(state.prop_rep[util.Party.OTHER]/(state.delegation*2)))
        print(state.prop_rep)

        totals[util.Party.DEM] += state.prop_rep[util.Party.DEM]
        totals[util.Party.GOP] += state.prop_rep[util.Party.GOP]
        totals[util.Party.OTHER] += state.prop_rep[util.Party.OTHER]

        print(state.check_prop())
    print("Total seats: D: {}, R: {}, I: {}".format(totals[util.Party.DEM],totals[util.Party.GOP],totals[util.Party.OTHER]))

    old_colors = {}
    prop_colors = {}
    for s in states:
        state = states[s]
        try:
            old_colors[s] = mapwriter.lean_to_color(state.rep_shares(),
                                                    state.voteshare, state.delegation)

            prop_colors[s] = mapwriter.lean_to_color({p: state.prop_rep[p]/(2*state.delegation) for p in list(util.Party)}, state.voteshare, state.delegation*2)
        except:
            print("Error on {}".format(str(state)))
            exit()

    oldmap = mapwriter.MapWriter(old_colors)
    oldmap.generate()
    oldmap.write("out/{}_old_map.svg".format(year))
    prop_map = mapwriter.MapWriter(prop_colors)
    prop_map.generate()
    prop_map.write("out/{}_prop_map.svg".format(year))

    if (args.latex):
        header = [['\\textbf{State}', '\\multicolumn{3}{c}{\\textbf{Single Member Districts}}',
                   '\\multicolumn{3}{c}{\\textbf{Mixed Member Prop.}}'],
                  ['', 'GOP', 'Dem', 'Badness', 'GOP', 'Dem', 'Badness']]

        data = []
        total_seats = {'gop_old': 0, 'dem_old': 0, 'gop_prop': 0, 'dem_prop': 0}
        for s in states:
            state = states[s]
            vote_share = state.voteshare
            rep_share = state.rep_shares()
            prop_share = {p: state.prop_rep[p]/(2*state.delegation) for p in list(util.Party)}

            def countreps(p):
                i=0
                for r in state.reps:
                    if r.party == p:
                        i+=1
                return i

            rep_dist = {p: countreps(p) for p in list(util.Party)}
            prop_dist = state.prop_rep

            total_seats['gop_old'] += rep_dist[util.Party.GOP]
            total_seats['dem_old'] += rep_dist[util.Party.DEM]
            total_seats['gop_prop'] += prop_dist[util.Party.GOP]
            total_seats['dem_prop'] += prop_dist[util.Party.DEM]

            data.append([state.name,'{}'.format(rep_dist[util.Party.GOP]),
                                    '{}'.format(rep_dist[util.Party.DEM]),
                                    '{:.1f}\\%'.format(vote_badness(rep_share, vote_share)*100.0),
                                    '{}'.format(prop_dist[util.Party.GOP]),
                                    '{}'.format(prop_dist[util.Party.DEM]),
                                    '{:.1f}\\%'.format(vote_badness(prop_share, vote_share)*100.0)])


        footer = [['Totals',
         str(total_seats['gop_old']), str(total_seats['dem_old']),
        '{:.1f}\\%'.format(vote_badness({util.Party.GOP: total_seats['gop_old']/435.0,
                                        util.Party.DEM: total_seats['dem_old']/435.0},
                                    YEAR_DATA[year]['results'])*100.0),

        str(total_seats['gop_prop']), str(total_seats['dem_prop']),
        '{:.1f}\\%'.format(vote_badness({util.Party.GOP: total_seats['gop_prop']/870.0,
                                        util.Party.DEM: total_seats['dem_prop']/870.0},
                                    YEAR_DATA[year]['results'])*100.0)]]


        with open("out/{}_table.tex".format(year), "w") as tfile: tfile.write(latex.table(header, data, footer, 8))
        os.system('pdflatex out/test.tex')

def vote_badness(rep_shares, vote_shares):
    dem_diff = rep_shares[util.Party.DEM] - vote_shares[util.Party.DEM]
    gop_diff = rep_shares[util.Party.GOP] - vote_shares[util.Party.GOP]
    return ((dem_diff**2/2 + gop_diff**2/2)**0.5)


if __name__=="__main__":
    main()
