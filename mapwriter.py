import us
import xml
import xml.etree.ElementTree as ET
import util

def lean_to_color(rep_share, vote_share, delegation):
    diff = {key: (rep_share[key]-vote_share[key])/(vote_share[util.Party.GOP]+vote_share[util.Party.DEM]) for key in rep_share if key in vote_share}
    color = ''
    rep_diff = diff[util.Party.GOP]-diff[util.Party.DEM]
    if rep_diff > 0:
        color = '#FF{0:02X}{0:02X}'.format(abs(255-int(255*rep_diff)))
    else:
        color = '#{0:02X}{0:02X}FF'.format(abs(255-int(-255*rep_diff)))
    return color


class MapWriter(object):
    blankFile = "electoral_map.svg"
    def __init__(self, colors):
        self.state_colors = {}
        for c in colors:
            self.state_colors[MapWriter.state_to_abbr(c)] = colors[c]
        self.map = ET.parse(MapWriter.blankFile)
        self.mapRoot = self.map.getroot()

    def generate(self):
        for i in self.mapRoot:
            if (i.attrib == {'id': 'outlines'}):
                for j in i:
                    state = j.attrib['id']
                    j.set('fill', self.state_colors[state])
                    j.set('style', 'stroke-width:2;stroke-miterlimit:4;stroke-dasharray:none;stroke:#000000;stroke-opacity:1')
                break

    def write(self, filename):
        self.map.write(filename)




    @staticmethod
    def state_to_abbr(state_name):
        return us.states.mapping('name', 'abbr')[state_name]
