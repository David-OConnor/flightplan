import os
import xml.etree.ElementTree as ET
import zipfile

import requests

from diverts.models import Airfield, Runway, Navaid


#todo allow for bearing/dist cuts from navaids in flightplan

DIR = os.path.dirname(__file__)
DIR_RES = os.path.abspath(os.path.join(DIR, 'resources'))



def parse_lat_lon(lat_lon: ET.Element) -> (float, float):
    """Remove the extended 'aixm' tag, leaving only 'Navaid', 'VOR' etc."""
    lat_lon = lat_lon[0].text.split(' ')
    lat = float(lat_lon[0])
    lon = float(lat_lon[1])
    return lat, lon


def populate_airfields(filename):
    #todo do I need to filter tby timeslice, or can Icut it out?
    aixm = '{http://www.aixm.aero/schema/5.1}'  # make these global?
    gml = '{http://www.opengis.net/gml/3.2}'

    tree = ET.parse(os.path.join(DIR_RES, filename))
    root = tree.getroot()

    # tags: AirportHeliport, OrganisationAuthority, Unit, RadioCommunicationChannel,
    # AirTrafficControlService, Runway, RunwayMarking, TouchDownLiftOff,
    # RunwayDirection, Glidepath, AIrportSuppliesService,

    for child in root:
        if child[0].tag == '{0}AirportHeliport'.format(aixm):
            ident = child.findall(".//{0}timeSlice//{0}designator".format(aixm))
            name = child.findall(".//{0}timeSlice//{0}name".format(aixm))
            control = child.findall(".//{0}timeSlice//{0}controlType".format(aixm))
            lat_lon = child.findall(".//{0}pos".format(gml))

            ident = ident[0].text
            name = name[0].text
            try:
                control = control[0].text
            except IndexError:
                control = ''
            lat, lon = parse_lat_lon(lat_lon)

            # yield("airfield", ident, name, control, lat, lon)

            a = Airfield(ident=ident, name=name, control=control, lat=lat, lon=lon)
            a.save()

        elif child[0].tag == '{0}Runway'.format(aixm):
            airfield_id = child.findall(".//{0}timeSlice//{0}associatedAirportHeliport".format(aixm))
            # airfield = Airfield('asfd')
            number = child.findall(".//{0}timeSlice//{0}designator".format(aixm))
            length = child.findall(".//{0}timeSlice//{0}lengthStrip".format(aixm))
            width = child.findall(".//{0}timeSlice//{0}widthStrip".format(aixm))

            # Parses a dict with one k/v. We only care about the v.
            # airfield_id is the internal AIXM id, ie 'AH_0000001'. airfield_ident
            # is the airfield identifier, ie 'ADK'.
            airfield_id = list(airfield_id[0].attrib.values())[0]
            airfield_id = airfield_id.split("'")[1]
            airfield_elem = root.findall(
                ".//{0}AirportHeliport[@{1}id='{2}']".format(aixm, gml, airfield_id))
            airfield_ident = airfield_elem[0].findall(".//{0}designator".format(aixm))[0].text
            airfield = Airfield.objects.get(ident=airfield_ident)

            number = number[0].text

            # Temp code - ruways show as '5/23', then separate entries for 5 and
            # 23. Only the'5/23' entry has length and width
            try:
                length = int(length[0].text)
                width = int(width[0].text)
            except IndexError:
                continue

            # yield("rwy", airfield_id, number, length, width)

            r = Runway(airfield=airfield, number=number, length=length, width=width)
            r.save()


def populate_navaids(filename):
    """placeholder"""
    faa = '{http://www.faa.gov/aixm5.1}'  # set these dynamically
    aixm = '{http://www.aixm.aero/schema/5.1}'
    gml = '{http://www.opengis.net/gml/3.2}'

    # The source document appears to include navaids, organizational authorities,
    # DMEs, NDBs, VORs, TACANs and Information Services, and radio communication channels.
    # Only pull data from categories related to navaids.

    possible_components = ['VOR', 'TACAN', 'DME', 'NDB']

    tree = ET.parse(os.path.join(DIR_RES, filename))
    root = tree.getroot()

    for child in root:
        # Skip non-navaid entries, like information services and org authorities.
        if child[0].tag != '{0}Navaid'.format(aixm):
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
            # Parses a dict with one k/v. We only care about the v.
            comp_id = list(equip.attrib.values())[0]

            for comp in possible_components:
                if comp in comp_id:
                    comps.append(comp)
        # The later chunk of the admin file switches to localizers/glidepaths
        # etc, and still refers to them as Navaids.  They won't have idents, names,
        # elevated point coords etc.  Skip them. Error checking on the ident is
        # good enough.
        try:
            ident = ident[0].text
        except IndexError:
            continue

        name = name[0].text

        lat, lon = parse_lat_lon(lat_lon)


        # yield (ident, name, comps, lat, lon)  # temp
        n = Navaid(ident=ident, name=name, components=comps, lat=lat, lon=lon)
        n.save()



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