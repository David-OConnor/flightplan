import os
import xml.etree.ElementTree as ET
import zipfile

import requests

from diverts.models import Airfield, Runway, Navaid


#todo allow for bearing/dist cuts from navaids in flightplan

DIR = os.path.dirname(__file__)
DIR_RES = os.path.abspath(os.path.join(DIR, 'resources'))

aixm = '{http://www.aixm.aero/schema/5.1}'  # make these global?
gml = '{http://www.opengis.net/gml/3.2}'
faa = '{http://www.faa.gov/aixm5.1}'  # set these dynamically


def parse_lon_lat(lon_lat: ET.Element) -> (float, float):
    """Remove the extended 'aixm' tag, leaving only 'Navaid', 'VOR' etc."""
    lon_lat = lon_lat[0].text.split(' ')
    lon = float(lon_lat[0])
    lat = float(lon_lat[1])
    return lat, lon


def populate_airfields(filename):
    """Save relevant airfield information to the database, from an AIXM xml file."""

    tree = ET.parse(os.path.join(DIR_RES, filename))
    root = tree.getroot()

    # tags: AirportHeliport, OrganisationAuthority, Unit, RadioCommunicationChannel,
    # AirTrafficControlService, Runway, RunwayMarking, TouchDownLiftOff,
    # RunwayDirection, Glidepath, AirportSuppliesService,

    for child in root:
        if child[0].tag == '{0}AirportHeliport'.format(aixm):
            ident = child.findall("./{0}AirportHeliport/{0}timeSlice/{0}AirportHeliportTimeSlice/{0}designator".format(aixm))
            name = child.findall("./{0}AirportHeliport/{0}timeSlice/{0}AirportHeliportTimeSlice/{0}name".format(aixm))
            lon_lat = child.findall("./{0}AirportHeliport/{0}timeSlice/{0}AirportHeliportTimeSlice/{0}ARP/{0}ElevatedPoint/{1}pos".format(aixm, gml))
            aixm_id = child.findall("./{0}AirportHeliport".format(aixm))

            ident = ident[0].text
            name = name[0].text
            aixm_id = list(aixm_id[0].attrib.values())[0]

            lat, lon = parse_lon_lat(lon_lat)

            # yield("airfield", ident, name, lat, lon)

            a = Airfield(ident=ident, name=name, aixm_id=aixm_id, lat=lat, lon=lon)
            a.save()


def populate_runways(filename):
    """Save relevant runway information to the database, from an AIXM xml file."""
    # Uses the same AIXM file as airfields (APT_AIXM.xml)
    # Must be run after populate_airfields, or the Airfield foreign keys won't
    # have anything to relate to.

    tree = ET.parse(os.path.join(DIR_RES, filename))
    root = tree.getroot()

    for child in root:
        if child[0].tag == '{0}Runway'.format(aixm):
            aixm_id = child.findall("./{0}Runway/{0}timeSlice/{0}RunwayTimeSlice/{0}associatedAirportHeliport".format(aixm))
            number = child.findall("./{0}Runway/{0}timeSlice/{0}RunwayTimeSlice/{0}designator".format(aixm))
            length = child.findall("./{0}Runway/{0}timeSlice/{0}RunwayTimeSlice/{0}lengthStrip".format(aixm))
            width = child.findall("./{0}Runway/{0}timeSlice/{0}RunwayTimeSlice/{0}widthStrip".format(aixm))

            # Parses a dict with one k/v. We only care about the v.
            # airfield_id is the internal AIXM id, ie 'AH_0000001'. airfield_ident
            # is the airfield identifier, ie 'ADK'.
            aixm_id = list(aixm_id[0].attrib.values())[0]
            aixm_id = aixm_id.split("'")[1]

            #todo this is the only line that makes it slow!
            # airfield_elem = root.findall("./{3}Member/{0}AirportHeliport[@{1}id='{2}']".format(aixm, gml, aixm_id, faa))

            # airfield_ident = airfield_elem[0].findall(".//{0}designator".format(aixm))[0].text
            airfield = Airfield.objects.get(aixm_id=aixm_id)

            number = number[0].text

            # Ruways show as '5/23', then separate entries for 5 and
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
    """Save relevant navaid information to the database, from an AIXM xml file."""

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

        # ident = child.findall(".//{0}designator".format(aixm))
        # name = child.findall(".//{0}name".format(aixm))
        # lon_lat = child.findall(".//{0}pos".format(gml))
        # equipment = child.findall(".//{0}theNavaidEquipment".format(aixm))

        ident = child.findall("./{0}Navaid/{0}timeSlice/{0}NavaidTimeSlice/{0}designator".format(aixm))
        name = child.findall("./{0}Navaid/{0}timeSlice/{0}NavaidTimeSlice/{0}name".format(aixm))
        lon_lat = child.findall("./{0}Navaid/{0}timeSlice/{0}NavaidTimeSlice/{0}location/{0}ElevatedPoint/{1}pos".format(aixm, gml))
        equipment = child.findall("./{0}Navaid/{0}timeSlice/{0}NavaidTimeSlice/{0}navaidEquipment/{0}NavaidComponent/{0}theNavaidEquipment".format(aixm))

        # This method seems messy, but avoids finding the separate top-level
        # component, and pulling data from it. We only need the types of components
        # per Navaid.
        comps = []

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

        lat, lon = parse_lon_lat(lon_lat)

        # yield (ident, name, comps, lat, lon)  # temp
        n = Navaid(ident=ident, name=name, components=comps, lat=lat, lon=lon)
        n.save()


def populate_all():
    populate_navaids('NAV_AIXM.xml')
    populate_airfields('APT_AIXM.xml')
    populate_runways('APT_AIXM.xml')


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