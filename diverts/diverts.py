import os
import xml.etree.ElementTree as ET
import zipfile

import requests

from diverts.models import Airfield, Navaid


DIR = os.path.dirname(__file__)
DIR_RES = os.path.abspath(os.path.join(DIR, 'resources'))



def populate_navaids(filename):
    """placeholder"""
    faa = '{http://www.faa.gov/aixm5.1}'  # set these dynamically
    aixm = '{http://www.aixm.aero/schema/5.1}'
    gml = '{http://www.opengis.net/gml/3.2}'

    # The source document appears to include navaids, organizational authorities,
    # DMEs, NDBs, VORs, TACANs and Information Services, and radio communication channels.
    # Only pull data from categories related to navaids.

    possible_components = ['VOR', 'TACAN', 'DME', 'NDB']

    navaid_cats = [
        '{0}Navaid'.format(aixm),
        '{0}VOR'.format(aixm),
        '{0}TACAN'.format(aixm),
        '{0}DME'.format(aixm),
        '{0}NDB'.format(aixm)
    ]

    navaid_cats = ['{0}Navaid'.format(aixm)]

    tree = ET.parse(os.path.join(DIR_RES, filename))
    root = tree.getroot()

    for child in root:
        # Skip non-navaid entries, like information services and org authorities.
        if child[0].tag not in navaid_cats:
            continue

        ident = child.findall(".//{0}timeSlice//{0}designator".format(aixm))
        name = child.findall(".//{0}timeSlice//{0}name".format(aixm))
        lat_lon = child.findall(".//{0}pos".format(gml))

        # This method seems messy, but avoids finding the separate top-level
        # component, and pulling data from it. We only need the types of components
        # per Navaid.
        comps = []
        equipment = child.findall(".//{0}theNavaidEquipment".format(aixm))
        for equip in equipment:
            # Returns a dict with one k/v. We only care about the v.
            id_ = equip.attrib
            id_ = list(id_.values())[0]

            for comp in possible_components:
                if comp in id_:
                    comps.append(comp)

        try:
            ident = ident[0].text
        except IndexError:
            ident = ''

        try:
            name = name[0].text
        except IndexError:
            name = ''

        # Remove the extended 'aixm' tag, leaving only 'Navaid', 'VOR' etc.
        # category = child[0].tag.split('}')[1]

        try:
            lat_lon = lat_lon[0].text
            split = lat_lon.split(' ')
            lat = float(split[0])
            lon = float(split[1])
        except IndexError:
            lat = 0
            lon = 0



        yield (ident, name, comps, lat, lon)  # temp

        n = Navaid(ident=ident, lat=lat, lon=lon)
        n.save()


def parse_xml_with_keys(pefix, *keys):
    pass







def download_data():
    """Downloads NFDC data"""
    date = '2014-07-24'  # Start date
    url = 'https://nfdc.faa.gov/webContent/56DaySub/{0}/aixm5.1.zip'.format(date)
    web_file = requests.get(url).content

    with open(os.path.join(DIR_RES, 'aixm5.1.zip'), 'wb') as f:
        f.write(web_file)

    with zipfile.ZipFile(os.path.join(DIR_RES, 'AIXM_5.1.zip', 'w')) as myzip:
        myzip.write()

        # move to database




#order:
#NAvaid,
#Org auth
#ndb
#dme
#rcc
#is

