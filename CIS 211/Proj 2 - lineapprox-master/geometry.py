"""
Geometry:  Points and polylines, including
approximation using the Ramer-Douglas-Peucker
algorithm.   

This is a 'model' component and should not directly 
contain any graphics code. All coordinates are in the 
model coordinate system.  The unit of the coordinate 
system can be any metric (cm, meters, whatever), but 
it must be the same unit in the x and y dimension 
so that the the usual distance formula holds.  Note that 
this IS true of UTM coordinates but it is NOT true of 
latitude and longitude. 

Class PolyLine is the representation of a sequence of 
points.  Includes hooks for a view component. 

Events generated (for view components): 
   "trial_approx" with options = { "p1": (x,y), "p2": (x,y) }
   "final_approx_seg" with options = { "p1": (x,y), "p2": (x,y) }

A trial approximation (event "trial_approx") is a segment that may 
be further subdivided.  A final approximation (event "final_approx_seg")
is a segment that will be incorporated in the line approximation with 
no further refinement.  

Author: Noah Tigner

"""
import math

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

class PolyLine:
    """A polyline is a sequence of points, represented 
    as (x,y) tuples.

    PolyLine.points and PolyLine.approx are public, read-only 
    attributes.  Other attributes are private. 
    """

    def __init__(self, points):
        self.points = points
        self.listeners = [ ]
        # Initially, the approximated version of the polyline
        # is the same as the original polyline.  Initially the
        # approximation accuracy is zero, i.e., the approximate
        # points are within distance 0 of the original points. 
        self.approx = points
        self.tolerance = 0

    def add_listener(self, listener):
        self.listeners.append(listener)

    def notify_all(self, event_name, options={}):
        for listener in self.listeners:
            listener.notify(event_name, options=options)

    def simplify(self, tolerance):
        """Approximate the polyline, within a maximum deviation
        of the specified tolerance distance, with as few points
        as possible. 
        """
        log.debug("Top-level call to simplify")
        self.tolerance = tolerance 
        self.approx = [ ]
        self._dp_simplify(0, len(self.points)-1)

        self.approx.append(self.points[-1])
        return

    def _dp_simplify(self, from_index, to_index):
        """Recursively build up simplified path, working left to 
        right to add the resulting points to the simplified list. 
        Generates events 'trial_approx' and 'final_approx_seg' 
        with options p1=(x,y), p2=(x,y), which may be used by a 
        view component for animation.
        """
        log.debug("dp {}-{} {}-{}"
                      .format(from_index,to_index,
                                  self.points[from_index],
                                  self.points[to_index]))
        self.notify_all("trial_approx",
                            options = { "p1": self.points[from_index],
                                        "p2": self.points[to_index] })
        log.debug("Returning with simplified = {}".format(self.approx))

        if to_index - from_index < 2: # Base 1: 2 point
            self.approx.append(self.points[from_index])
            self.notify_all("final_approx_seg",
                            options = {"p1": self.points[from_index],
                                       "p2": self.points[to_index]})
            return

        seg_start = self.points[from_index]
        seg_end = self.points[to_index]
        max_deviation = self.tolerance

        for i in range(from_index + 1, to_index):
            dev = deviation(seg_start, seg_end, self.points[i])
            if dev > max_deviation:
                max_deviation = dev
                max_index = i

        if max_deviation > self.tolerance: # Inductive Case
            self._dp_simplify(from_index, max_index)
            self._dp_simplify(max_index, to_index)

        else: # Base 2: max deviation < tolerance for all points
            self.approx.append(self.points[from_index])
            self.notify_all("final_approx_seg",
                            options={"p1": self.points[from_index],
                                    "p2": self.points[to_index]})


        
def deviation(p1, p2, p):
    """Shortest distance from point px to a line 
    that passes through p1 and p2.
    p1, p2, px represented as (x,y). 
    """
    ix, iy = normal_intercept(p1, p2, p)
    # Standard distance formula, sqrt((x2-x1)^2 +(y2-y1)^2)
    log.debug("Computing distance from {} to {}"
                  .format(p, (ix,iy)))
    px, py = p
    dx = ix - px
    dy = iy - py
    return math.sqrt(dx*dx + dy*dy)

def normal_intercept(p1, p2, p):
    """
    The point at which a line through p1 and p2 
    intersects a normal dropped from p.  See normals.md
    for an illustration. 
    """
    log.debug("Normal intercept {}-{} from {}"
                  .format(p1, p2, p))
    p1_x, p1_y = p1
    p2_x, p2_y = p2
    px, py = p

    # Special cases: slope or normal slope is undefined
    # for vertical or horizontal lines, but the intersections
    # are trivial for those cases
    if p2_x == p1_x:
        log.debug("Intercept at {}".format((p1_x,py)))
        return p1_x, py
    elif p2_y == p1_y:
        log.debug("Intercept at {}".format((px, p1_y)))
        return px, p1_y

    # The slope of the segment, and of a normal ray
    seg_slope = (p2_y - p1_y)/(p2_x - p1_x)
    normal_slope = 0 - (1.0 / seg_slope)

    # For y=mx+b form, we need to solve for b (y intercept)
    seg_b = p1_y - seg_slope * p1_x
    normal_b = py - normal_slope * px

    #log.debug("Segment line is y= {} * x + {}".format(seg_slope, seg_b))
    #log.debug("Normal line is  y= {}  *x + {}".format(normal_slope, normal_b))

    # Combining and subtracting the two line equations to solve for
    x_intersect = (seg_b - normal_b) / (normal_slope - seg_slope)
    y_intersect = seg_slope * x_intersect + seg_b
    # Colinear points are ok!

    log.debug("Intercept at {}".format(x_intersect, y_intersect))
    return (x_intersect, y_intersect)



    
    
