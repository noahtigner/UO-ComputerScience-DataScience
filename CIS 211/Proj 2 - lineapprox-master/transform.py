"""
A Transform is used to map a point or sequence of 
points from some model space (also called "world coordinates")
into view space ("window coordinates"). 

"""

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

class Transform(object):
    """A Transform maps a set of world coordinate pairs into 
    window coordinates by scaling and translation. 
    """

    def __init__(self, uniform=True, y_flip=True, 
                     to_ll=(0,0), to_ur=(100,100),
                     from_ll=(0,0), from_ur=(100,100)):
        """Create a transformation from model coordinates
        with x and y ranging from from_ll to from_ur
        to window coordinates to_ll to to_ur.  y_flip 
        indicates that model coordinate y axis goes up, 
        window coordinate y axis goes down. 
        """
        from_ll_x, from_ll_y = from_ll
        to_ll_x, to_ll_y = to_ll
        from_ur_x, from_ur_y = from_ur
        to_ur_x, to_ur_y = to_ur
    
        if y_flip:
            # Reverse y axis
            to_ll_y, to_ur_y = to_ur_y, to_ll_y

        sfx = (to_ur_x - to_ll_x) / (from_ur_x - from_ll_x)
        sfy = (to_ur_y - to_ll_y) / (from_ur_y - from_ll_y)

            
        log.debug("Scale factor x {}, Scale factor y {}".format(sfx,sfy))

        if uniform and y_flip: 
            sfx = min(sfx, -sfy)
            sfy = max(-sfx, sfy)
        elif uniform:
            sfx = min(sfx, sfy)
            sfy = min(sfx, sfy)            
            log.debug("Adjusted scale factor x {}, Scale factor y {}"
                        .format(sfx,sfy))

        # Scale factors
        self.sfx = sfx
        self.sfy = sfy
        # Translation
        self.to_ll_x = to_ll_x
        self.to_ll_y = to_ll_y
        self.from_ll_x = from_ll_x
        self.from_ll_y = from_ll_y

    def transform(self, points):
        """Apply transform to a list of points, or to 
        a single point (x,y).
        """
        scaled = [ ]
        for pt in points:
            scaled_pt = self.transform_pt(pt)
            scaled.append(scaled_pt)
        return scaled

    def transform_pt(self, pt):
        """Apply transformation to a single point"""
        x, y = pt
        x_scaled = self.to_ll_x + self.sfx * (x - self.from_ll_x)
        y_scaled = self.to_ll_y + self.sfy * (y - self.from_ll_y)
        return x_scaled, y_scaled


def bbox(points):
    """Find the bounding box of a set of points. 
    Typically used to find the range of model coordinates
    for initializing a Transform. 
    Points is a sequence of (x,y) pairs (at least 1). 
    Return the (x_min, y_min) and (x_max, y_max) 
    from the points. 
    """
    assert len(points) > 0
    x_min, y_min = points[0]
    x_max, y_max = points[0]
    for pt in points:
        x,y = pt
        if x < x_min: x_min = x
        if y < y_min: y_min = y
        if x > x_max: x_max = x
        if y > y_max: y_max = y
    log.debug("Points bounded by ({},{}) and ({},{})"
                  .format(x_min, y_min, x_max, y_max))
    return (x_min, y_min), (x_max, y_max)


