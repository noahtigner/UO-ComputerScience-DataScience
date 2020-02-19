"""
View (animate) line simplification using the 
Douglas-Peucker (aka Ramer-Douglas-Peucker) 
algorithm. Implemented as a view object so that 
we can keep the canvas and coordinate transforms
as object state to be applied consistently. 
"""

import graphics.graphics as graphics
import transform

class View(object):
    """A view of line simplification"""

    def __init__(self, win, points, margin=20, color="blue"):
        self.win = win
        pts_ll, pts_ur = transform.bbox(points)
        # Map easting,northing coordinates into window coordinates,
        #   scaling x and y coordinates uniformly and flipping the
        #   y axis so that north = up 
        self.tx = transform.Transform(
            from_ll = pts_ll, from_ur = pts_ur,
            to_ll = (margin, margin),
            to_ur = (win.width - margin, win.height - margin),
            uniform=True, y_flip=True
            )
        self.view_original = graphics.PolyLine(self.tx.transform(points))
        self.view_original.setOutline(color)
        self.view_original.draw(self.win)

    def notify(self, event_name, options):
        """Event notifications from simplification process."""
        if event_name == "trial_approx":
            p1 = options["p1"]
            p2 = options["p2"]
            self.draw_segment(p1, p2, color="grey")
        elif event_name == "final_approx_seg":
            p1 = options["p1"]
            p2 = options["p2"]
            self.draw_segment(p1, p2, color="red")
        else:
            raise Exception("Unknown event {}".format(event_name))

    def draw_segment(self, p1, p2, color="green"):
        """Draw segment between two points. Returns an identifier
        that can be used to erase that segment later.
        """
        p1_x, p1_y = self.tx.transform_pt(p1)
        p2_x, p2_y = self.tx.transform_pt(p2)
        seg = graphics.Line(graphics.Point(p1_x, p1_y),
                                graphics.Point(p2_x, p2_y))
        seg.setOutline(color)
        seg.draw(self.win)
        return seg

    
        


