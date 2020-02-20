#! /usr/bin/env python3
#
"""
Convert a GPX file to a sequence of 
points in UTM form

"""

# Load modules from ./lib
import sys
import argparse
import gpxpy
import gpxpy.gpx
import utm
import json

import logging
logging.basicConfig(format='%(levelname)s:%(message)s',
                        level=logging.DEBUG)
log = logging.getLogger(__name__)

def getargs():
    """Return arguments as a NameSpace object"""
    parser = argparse.ArgumentParser("Simplify GPX files")
    parser.add_argument('infile',
        type=argparse.FileType(mode='r', encoding="utf-8", errors="replace"), 
        help="The GPX input file")
    parser.add_argument('outfile', 
        type=argparse.FileType(mode='w', encoding="utf-8"),
        help="Output to this file")
    parser.add_argument("--delta", dest="delta", type=int, default=None,
                            help="Max deviation from input route, in meters")
    argvals = parser.parse_args()
    return argvals

def points(gpx_obj):
    """
    Extract all the track points from a gpx object.
    Returns a list of points.
    """
    li = [ ] 
    for track in gpx_obj.tracks:
        for segment in track.segments:
            for point in segment.points:
                li.append([point.latitude, point.longitude])
    return li

def track_centerpoint(track):
    """Given track == [[lat, lon], [lat, lon], ... ], 
    return (midlat, midlon) as central values, i.e., 
    midlat is halfway between min and max of lat, and midlon is 
    halfway between min and max of lon.
    """
    if len(track) == 0:
        return (0, 0)
    elif len(track) == 1:
        return track[0]
    min_lat, min_lon = track[0]
    max_lat, max_lon = track[0]
    for pt in track:
        lat, lon = pt
        if lat < min_lat:
            min_lat = lat
        if lat > max_lat:
            max_lat = lat
        if lon < min_lon:
            min_lon = lon
        if lon > max_lon:
            max_lon = lon
    return (min_lat + max_lat)/2.0, (min_lon + max_lon)/2.0



def track_to_utm(track):
    """convert [[lat, lon], [lat, lon], ... ]
    or [(lat, lon), (lat, lon), ... )
    to [(easting, northing), (easting, northing), ...], zone.
    We choose one UTM zone and make sure all eastings and 
    northings are in that zone, so that all points are compatible 
    for distance calculations. 
    """
    if len(track) == 0:
        return track, 10 

    # Determine UTM zone from center of path
    mid_lat, mid_lon = track_centerpoint(track)
    _, _, utm_zone, _ = utm.from_latlon(mid_lat, mid_lon)

    utm_path = [ ]

    for pt in track:
        lat, lon = pt
        easting, northing, _, _ = \
          utm.from_latlon(lat, lon, force_zone_number=utm_zone)
        # Compact rep in text: Round meters for easting and northing
        utm_pt = (round(easting), round(northing))
        utm_path.append(utm_pt)

    return utm_path, utm_zone

def dump_csv(points, file=sys.stdout):
    """Given [(easting, northing), (easting, northing), ... ]
    write CSV file in which eastings are a column and northings 
    are a column. 
    """
    print("Easting,Northing", file=file)
    for easting, northing in points:
        print("{},{}".format(easting, northing), file=file)

def main():
    args = getargs()
    gpx = gpxpy.parse(args.infile)
    delta = args.delta
    log.debug("{} points before simplification".format(len(points(gpx))))
    if delta: 
        gpx.simplify(delta)
        log.debug("{} points after simplification".format(len(points(gpx))))
    latlon_points = points(gpx)
    utm_path, utm_zone = track_to_utm(latlon_points)
    dump_csv(utm_path, args.outfile)
    
if __name__ == "__main__":
    main()




