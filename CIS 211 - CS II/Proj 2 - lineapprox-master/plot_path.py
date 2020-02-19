"""
Plot a list of points in a TkInter window 
(using Zelle graphics package).  Class 
Transform provides scaling and translation to fit
a set of points in a region of a window. 

"""

import graphics.graphics as graphics
import argparse
import view_simplify
import geometry

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

def plot_path(win, points, width=None, height=None):
    """
    We have a window with some width and height.  We have 
    a sequence of (x,y) pairs that probably don't fit in the 
    window coordinate space.  No prob ... we'll project 
    into that space and draw the projected path.  
    """
    # Default to window size

def cli():
    """Command line arguments for plotting a CSV file of points"""
    parser = argparse.ArgumentParser("Plot from CSV")
    parser.add_argument(
        "csv", type=argparse.FileType('r'),  
        help="Path to CSV file of points")
    parser.add_argument(
        "width", type=int, default=300, 
        help="Window width, in pixels")
    parser.add_argument(
        "height", type=int, default=300,
        help="Window height, in pixels")
    parser.add_argument(
        "tolerance", type=int, default=1000,
        help="Error tolerance in meters")
    args = parser.parse_args()
    return args

def read_points(csv_file):
    """Each line in the CSV file should contain an 
    easting and a northing in columns 0 and 1.  The first
    row may be column headers, so we'll skip any non-numeric 
    entries.
    """
    points = [ ]
    for line in csv_file:
        fields = line.split(",")
        if len(fields) < 2:
            continue
        easting = fields[0]
        northing = fields[1]
        if not easting.isdecimal():
            continue
        points.append((int(easting), int(northing)))
    return points


if __name__ == "__main__":
    args = cli()
    pts = read_points(args.csv)
    win = graphics.GraphWin("Sample", args.width, args.height)
    path = geometry.PolyLine(pts)
    log.debug("Will plot in area 0..{}, 0..{}"
                  .format(args.width,args.height))
    view = view_simplify.View(win, path.points)
    path.add_listener(view)
    input("Press enter to simplify")
    path.simplify(args.tolerance)
    print("Simplified from {} points to {} points"
              .format(len(path.points),len(path.approx)))
    input("Press enter to dismiss")
    
    

                          
    
