"""
Test suite for rects.py

"""
import unittest  # Python's native test harness
from rects import Rect, Point


class TestRects(unittest.TestCase):
    """A few unit tests for rects.py"""

    def test_no_overlap(self):
        """The intersection of non-overlapping rectangles
        should be an empty rectangle from (0,0) to (0,0)
        """
        r1 = Rect(Point(10, 10), Point(20, 20))
        r2 = Rect(Point(20, 20), Point(30, 30))
        empty = Rect(Point(0, 0), Point(0, 0))
        self.assertFalse(r1.overlaps(r2))
        self.assertEqual(r1.intersect(r2), empty)

    def test_some_overlap(self):
        """When there is an overlap, the intersection should be
        the region of overlap
        """
        r1 = Rect(Point(10, 10), Point(20, 20))
        r2 = Rect(Point(15, 15), Point(30, 30))
        self.assertTrue(r1.overlaps(r2))
        self.assertEqual(r1.intersect(r2), Rect(Point(15, 15), Point(20, 20)))

    def test_other_corners(self):
        """Rectangles are defined by lower left and upper right
        corners, even if the other two corners are provided.
        """
        self.assertEqual(Rect(Point(10, 10), Point(5, 15)),
                         Rect(Point(5, 10), Point(10, 15)))

    def test_bad_coords(self):
        """Point type constructor requires numeric coordinates;
        protects against wacky results because "50" > "100".
        (Regression test, this was causing failures when the
        driver program took strings from the command line.)
        """
        with self.assertRaises(AssertionError):
            r1 = Rect(Point("20", "20"), Point("100", "100"))
            r2 = Rect(Point("50", "50"), Point("200", "200"))


if __name__ == "__main__":
    unittest.main()
