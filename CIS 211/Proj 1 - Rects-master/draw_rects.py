"""
Draw rectangles
(driver program for rects.py)
"""
import graphics
import argparse
import rects

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 800


def cli():
    """Command line arguments for drawing two rectangles"""
    parser = argparse.ArgumentParser("Draw rectangles")
    parser.add_argument(
        "ll_x1", type=int,
        help="X coordinate (in pixels) of lower left corner, first rect")
    parser.add_argument(
        "ll_y1", type=int,
        help="Y coordinate (in pixels) of lower left corner, first rect")
    parser.add_argument(
        "ur_x1", type=int,
        help="X coordinate (in pixels) of upper right corner, first rect")
    parser.add_argument(
        "ur_y1", type=int,
        help="Y coordinate (in pixels) of upper right corner, first rect")
    parser.add_argument(
        "ll_x2", type=int,
        help="X coordinate (in pixels) of lower left corner, second rect")
    parser.add_argument(
        "ll_y2", type=int,
        help="Y coordinate (in pixels) of lower left corner, second rect")
    parser.add_argument(
        "ur_x2", type=int,
        help="X coordinate (in pixels) of upper right corner, second rect")
    parser.add_argument(
        "ur_y2", type=int,
        help="Y coordinate (in pixels) of upper right corner, second rect")
    args = parser.parse_args()
    return args


def draw_rect(canvas, rect, color="black"):
    """Draw the rectangle on the canvas"""
    log.debug("Drawing {}".format(repr(rect)))
    ll_view = graphics.Point(rect.ll.x, rect.ll.y)
    ur_view = graphics.Point(rect.ur.x, rect.ur.y)
    view = graphics.Rectangle(ll_view, ur_view)
    view.setFill(color)
    view.draw(canvas)


def main():
    """Draw two rectangles on a canvas"""
    args = cli()
    canvas = graphics.GraphWin("Rects", CANVAS_WIDTH, CANVAS_HEIGHT)
    r1 = rects.Rect(
        rects.Point(args.ll_x1, args.ll_y1),
        rects.Point(args.ur_x1, args.ur_y1))
    draw_rect(canvas, r1, color="red")
    log.info("Rectangle {}".format(r1))
    r2 = rects.Rect(
        rects.Point(args.ll_x2, args.ll_y2),
        rects.Point(args.ur_x2, args.ur_y2))
    draw_rect(canvas, r2, color="blue")
    log.info("Rectangle {}".format(r2))
    canvas.getMouse()
    r3 = r1.intersect(r2)
    print("Intersection: {}".format(r3))
    draw_rect(canvas, r3, color="purple")
    canvas.getMouse()   # Pause for user to click on screen
    canvas.close()


if __name__ == "__main__":
    main()
