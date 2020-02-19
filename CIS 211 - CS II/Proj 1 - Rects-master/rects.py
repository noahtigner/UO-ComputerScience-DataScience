"""
Rectangles:  Compute overlapping region of two rectangles.
  Point(x: number, y: number):  Cartesian coordinate pair
  Rect(ll: Point, ur: Point): A rectangle defined by lower left
     and upper right coordinates
     Rect.overlaps(other: Rect) -> boolean:  True if non-empty overlap
     Rect.intersect(other: Rect) -> Rect:
        region of intersection if non-empty,
        or empty Rect from 0,0 to 0,0 if not Rect.overlaps(other)

CIS 211 Project 1
Author:  Noah Tigner
UO email: nzt@uoregon.edu
"""

import numbers

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
# To turn on debugging output, change the above to
# log.setLevel(logging.DEBUG)


class Point(object):
    """A point is an ordered pair, (x,y)"""

    def __init__(self, x, y):
        assert isinstance(x, numbers.Number)
        assert isinstance(y, numbers.Number)
        self.x = x
        self.y = y
        log.debug("Created Point {}".format(repr(self)))

    def __repr__(self):
        return "Point({},{})".format(self.x, self.y)

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

    def __eq__(self, other):
        assert(isinstance(other, Point))
        return self.x == other.x and self.y == other.y


class Rect(object):
    """A rectangle identified by its lower left
    and upper right corners.
    """

    def __init__(self, ll, ur):
        """Initialize rectangle with ll and ur as corners."""
        log.debug("Rect from ll {}, ur {}".format(repr(ll), repr(ur)))
        # Ensure ll really is lower left and ur really is upper right
        self.ll = Point(min(ll.x, ur.x), min(ll.y, ur.y))
        log.debug("ll will be {}".format(self.ll))
        self.ur = Point(max(ll.x, ur.x), max(ll.y, ur.y))
        log.debug("ur will be {}".format(self.ur))
        log.debug("Created rect {}".format(repr(self)))

    def __repr__(self):
        return "Rect({},{})".format(self.ll, self.ur)

    def __str__(self):
        return "Rect({},{})".format(self.ll, self.ur)

    def __eq__(self, other):
        assert isinstance(other, Rect)
        return self.ll == other.ll and self.ur == other.ur

    def overlaps(self, other):
        """r1.overlaps(r2) if there is an area of positive
        size within r1 and also within r2.  "Of positive size"
        means that touching at a corner or along an edge is
        not enough ... the area of overlap must be positive.
        """

        if self.ll.x >= other.ur.x:
            return False
        
        if self.ll.y >= other.ur.y:
            return False
        
        if self.ur.x <= other.ll.x:
            return False
        
        if self.ur.y <= other.ll.y:
            return False
        
        return True
        
     
    def intersect(self, other):
        """Region of overlap, or (0,0),(0,0) if none"""
        
        if self.overlaps(other):
            return Rect(Point(max(self.ll.x, other.ll.x), max(self.ll.y, other.ll.y)),
                        Point(min(self.ur.x, other.ur.x), min(self.ur.y, other.ur.y)))


        else:
            return Rect(Point(0, 0), Point(0, 0))
