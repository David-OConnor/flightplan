from math import sin, asin, cos, acos, atan2, sqrt, radians, pi
import os
import xml.etree.ElementTree as ET
import zipfile

import requests
from django.db.models import Q
from django.db import DataError

from diverts.models import Airfield, Runway, Navaid, Fix


tau = pi * 2

#todo allow for bearing/dist cuts from navaids in flightplan

DIR = os.path.dirname(__file__)
DIR_RES = os.path.abspath(os.path.join(DIR, 'resources'))

aixm = '{http://www.aixm.aero/schema/5.1}'
gml = '{http://www.opengis.net/gml/3.2}'
faa = '{http://www.faa.gov/aixm5.1}'  # set these dynamically


#todo clean up repetatively calculating earth's radius

def ellipsoid_radius(f):
    # todo add this to shared_funcs
    #todo make shared_funcs its own module called geodesic
    #todo in shared funcs, switch to NM or nmi.
    # This doesn't quite match with Wolfram Alpha's results, but is closer
    # than using an average radius.
    # f is geodetic latitude, in degrees
    f = radians(f)
    a = 6378137.0  # m, per WGS84
    b = 6356752.31424518  # m, per WGS84
    #1/f = 298.257223563

    NM_per_m = .000539956803
    a, b = a * NM_per_m, b * NM_per_m

    return sqrt(((a**2 * cos(f))**2 + (b**2 * sin(f))**2) / ((a * cos(f))**2 + (b * sin(f))**2))


def find_brg(point0, point1):
    #todo copy+pasted from shared_funcs.py
    #todo: in shared_funcs.py, changed from a list to two separate args, like this is now.
    #todo ie replace it with this.
    """Find the bearing, in radians, between two points."""
    lat0 = radians(point0[0])
    lon0 = radians(point0[1])
    lat1 = radians(point1[0])
    lon1 = radians(point1[1])
    d_lon = lon1 - lon0

    brg = atan2(sin(d_lon)*cos(lat1), cos(lat0)*sin(lat1) - sin(lat0)*cos(lat1)*cos(d_lon))
    return (brg + tau) % tau


def cross_track_dist(point0: (float, float), point1: (float, float), third_point: (float, float)):
    #todo comment and clean this function.
    r = ellipsoid_radius(third_point[0])

    dist_start_third = find_dist(point0, third_point)
    dist_end_third = find_dist(point1, third_point)
    dist_start_end = find_dist(point0, point1)

    angular_start_third = (dist_start_third / (tau*r)) * tau
    angular_end_third = (dist_end_third / (tau*r)) * tau

    brg_start_third = find_brg(point0, third_point)
    brg_start_end = find_brg(point0, point1)

    cross_track = asin(sin(angular_start_third) * sin(brg_start_third - brg_start_end)) * r
    ang_ct = (cross_track / (tau*r)) * tau

    at_start = acos(cos(angular_start_third) / cos(ang_ct)) * r
    at_end = acos(cos(angular_end_third) / cos(ang_ct)) * r

    if at_start > dist_start_end:
        cross_track = find_dist(point1, third_point)
    elif at_end > dist_start_end:
        cross_track = find_dist(point0, third_point)

    return abs(cross_track)


def find_dist(point0: (float, float), point1: (float, float)):
    """Calculate the distance between two lat-lons, in nm.  Inputs are in degrees."""
    # todo add this to squadron's shared_funcs.py.
    lat0, lon0 = radians(point0[0]), radians(point0[1])
    lat1, lon1 = radians(point1[0]), radians(point1[1])
    r = ellipsoid_radius(lat0)

    dlon = lon1 - lon0
    dlat = lat1 - lat0

    a = (sin(dlat/2)) ** 2 + cos(lat0) * cos(lat1) * (sin(dlon/2)) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return r * c


def flight_path_js(flight_path):
    #todo use this to save repetative queries somehow with find_diverts?
    #todo route the reuslt thorugh views.py to only call this once?
    #todo this is straight up duplication of find_diverts first part.
    path_points = []
    for ident in flight_path:
        if len(ident) == 5:  # Fixes always have 5 characters. No others do.
            pt = Fix.objects.filter(ident=ident.upper())
        else:
            pt = Navaid.objects.filter(ident=ident.upper())
            if not pt:
                pt = Airfield.objects.filter(icao=ident.upper())
                if not pt:
                    pt = Airfield.objects.filter(ident=ident.upper())

        if not pt or len(pt) != 1:
            return
        pt = pt[0]

        try:
            ident = pt.icao
        except AttributeError:
            ident = pt.ident

        path_points.append([pt.lat, pt.lon, ident])
    return path_points


def find_diverts(flight_path: list, max_dist, min_rwy_len, min_rwy_width, paved_only) -> list:
    """Find divert airfields within a certain distance of the flight path that meet
    certain criteria, like min runway length."""
    path_points = []
    for ident in flight_path:
        # todo perhaps clean up this nest.
        if len(ident) == 5:  # Fixes always have 5 characters. No others do.
            pt = Fix.objects.filter(ident=ident.upper())
        else:
            pt = Navaid.objects.filter(ident=ident.upper())
            if not pt:
                pt = Airfield.objects.filter(icao=ident.upper())
                if not pt:
                    pt = Airfield.objects.filter(ident=ident.upper())

        if not pt or len(pt) != 1:
            return
        pt = pt[0]

        path_points.append((pt.lat, pt.lon))

    if paved_only:
        surface = Q(runway__surface='ASPH') | Q(runway__surface='CONC') | Q(runway__surface='OTHER')
    else:
        surface = ~Q(runway__surface='BARF')  # todo place holder
        # surface = Q(runway__surface='WATER')  # todo place holder

    # filters = {'runway__length__gte': min_rwy_len, 'runway__width__gte': min_rwy_width}

    # passed_rwy_len = Airfield.objects.filter(*surface, **filters).distinct()

    passed_rwy_len = Airfield.objects.filter(surface, runway__length__gte=min_rwy_len,
                                             runway__width__gte=min_rwy_width).distinct()

    result = []
    for airfield in passed_rwy_len:
        airfield_point = (airfield.lat, airfield.lon)
        #this bit shouldn't be necessary, as leg proximity includes it. Still sometimes coming ssort.
        if path_point_proximity(path_points, airfield_point, max_dist):
            result.append(airfield)
            continue

        if leg_proximity(path_points, airfield_point, max_dist):
            result.append(airfield)

    return result


def path_point_proximity(path_points, airfield_point, max_dist):
    for path_point in path_points:
        if find_dist(path_point, airfield_point) <= max_dist:
            return True
    return False


def leg_proximity(path_points, airfield_point, max_dist):
    legs = find_legs(path_points)
    for leg in legs:
        if cross_track_dist(leg[0], leg[1], airfield_point) <= max_dist:
            return True
    return False


def find_legs(path_points: list):
    """Return a list of tuples of points defining the start and end of each
    leg on a flight path."""
    if len(path_points) < 2:
        return

    result = [(path_points[0], path_points[1])]
    for point in path_points[1: -1]:
        result.append((point, path_points[path_points.index(point) + 1]))

    return result


def parse_lon_lat(lon_lat: ET.Element) -> (float, float):
    """Remove the extended 'aixm' tag, leaving only 'Navaid', 'VOR' etc."""
    lon_lat = lon_lat[0].text.split(' ')
    lon = float(lon_lat[0])
    lat = float(lon_lat[1])
    return lat, lon


def aixm_keys(element, keys: tuple):
    """Provides a cleaner API for parsing XML than creating the xpath strings manually."""
    path = '.'
    for key in keys:
        path += '/' + aixm + key
    return element.findall(path)


def populate_airfields(filename):
    """Save relevant airfield information to the database, from an AIXM xml file.
    Uses APT_AIXM.xml"""

    tree = ET.parse(os.path.join(DIR_RES, filename))
    root = tree.getroot()

    # tags: AirportHeliport, OrganisationAuthority, Unit, RadioCommunicationChannel,
    # AirTrafficControlService, Runway, RunwayMarking, TouchDownLiftOff,
    # RunwayDirection, Glidepath, AirportSuppliesService,

    for child in root:
        if child[0].tag == '{0}AirportHeliport'.format(aixm):
            ident = aixm_keys(child, ('AirportHeliport', 'timeSlice', 'AirportHeliportTimeSlice', 'designator'))
            icao = aixm_keys(child, ('AirportHeliport', 'timeSlice', 'AirportHeliportTimeSlice', 'locationIndicatorICAO'))
            name = aixm_keys(child, ('AirportHeliport', 'timeSlice', 'AirportHeliportTimeSlice', 'name'))
            lon_lat = child.findall("./{0}AirportHeliport/{0}timeSlice/{0}AirportHeliportTimeSlice/{0}ARP/{0}ElevatedPoint/{1}pos".format(aixm, gml))
            aixm_id = aixm_keys(child, ('AirportHeliport',))

            ident = ident[0].text
            try:  # Many smaller airfields don't have ICAO codes.
                icao = icao[0].text
            except IndexError:
                icao = ''
            name = name[0].text
            aixm_id = list(aixm_id[0].attrib.values())[0]

            lat, lon = parse_lon_lat(lon_lat)

            a = Airfield(ident=ident, icao=icao, name=name, aixm_id=aixm_id, lat=lat, lon=lon)
            a.save()


def populate_runways(filename):
    """Save relevant runway information to the database, from an AIXM xml file.
    Uses APT_AIXM.xml."""
    # Uses the same AIXM file as airfields (APT_AIXM.xml)
    # Must be run after populate_airfields, or the Airfield foreign keys won't
    # have anything to relate to.

    tree = ET.parse(os.path.join(DIR_RES, filename))
    root = tree.getroot()

    for child in root:
        if child[0].tag == '{0}Runway'.format(aixm):
            aixm_id = aixm_keys(child, ('Runway', 'timeSlice', 'RunwayTimeSlice', 'associatedAirportHeliport'))
            number = aixm_keys(child, ('Runway', 'timeSlice', 'RunwayTimeSlice', 'designator'))
            length = aixm_keys(child, ('Runway', 'timeSlice', 'RunwayTimeSlice', 'lengthStrip'))
            width = aixm_keys(child, ('Runway', 'timeSlice', 'RunwayTimeSlice', 'widthStrip'))
            surface = aixm_keys(child, ('Runway', 'timeSlice', 'RunwayTimeSlice', 'surfaceProperties', 'SurfaceCharacteristics', 'composition'))

            # Parses a dict with one k/v. We only care about the v.
            # airfield_id is the internal AIXM id, ie 'AH_0000001'. airfield_ident
            # is the airfield identifier, ie 'ADK'.
            aixm_id = list(aixm_id[0].attrib.values())[0]
            aixm_id = aixm_id.split("'")[1]

            airfield = Airfield.objects.get(aixm_id=aixm_id)

            number = number[0].text
            try:
                surface = surface[0].text
            except IndexError:  #todo figure out what this means
                surface = 'debug error'

            # Ruways show as '5/23', then separate entries for 5 and
            # 23. Only the'5/23' entry has length and width
            try:
                length = int(length[0].text)
                width = int(width[0].text)
            except IndexError:
                continue

            r = Runway(airfield=airfield, number=number, length=length, width=width, surface=surface)
            r.save()


def populate_navaids(filename):
    """Save relevant navaid information to the database, from an AIXM xml file.
    Uses NAV_AIXM.xml."""

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

        ident = aixm_keys(child, ('Navaid', 'timeSlice', 'NavaidTimeSlice', 'designator'))
        name = aixm_keys(child, ('Navaid', 'timeSlice', 'NavaidTimeSlice', 'name'))
        lon_lat = child.findall("./{0}Navaid/{0}timeSlice/{0}NavaidTimeSlice/{0}location/{0}ElevatedPoint/{1}pos".format(aixm, gml))
        equipment = aixm_keys(child, ('Navaid', 'timeSlice', 'NavaidTimeSlice', 'navaidEquipment', 'NavaidComponent', 'theNavaidEquipment'))

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

        n = Navaid(ident=ident, name=name, components=comps, lat=lat, lon=lon)
        try:
            n.save()
        except DataError:  # A single navaid, 'POE1', triggers this.
            pass


def populate_fixes(filename):
    #todo use class to reduce repetiion?
    """Save relevant fix information to the database, from an AIXM xml file.
    Uses AWY_AIXM.xml."""

    tree = ET.parse(os.path.join(DIR_RES, filename))
    root = tree.getroot()

    for child in root:
        # Skip non-fix entries.
        if child[0].tag != '{0}DesignatedPoint'.format(aixm):
            continue

        ident = aixm_keys(child, ('DesignatedPoint', 'timeSlice', 'DesignatedPointTimeSlice', 'name'))
        lon_lat = child.findall("./{0}DesignatedPoint/{0}timeSlice/{0}DesignatedPointTimeSlice/{0}location/{0}Point/{1}pos".format(aixm, gml))


        # todo Not sure what's triggering this.
        try:
            ident = ident[0].text
            lat, lon = parse_lon_lat(lon_lat)
        except IndexError:
            continue

        f = Fix(ident=ident, lat=lat, lon=lon)

        # Excludes oddballs like 'US Mexican Border.'
        try:
            f.save()
        except DataError:
            pass


def populate_all():
    populate_navaids('NAV_AIXM.xml')
    populate_fixes('AWY_AIXM.xml')
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