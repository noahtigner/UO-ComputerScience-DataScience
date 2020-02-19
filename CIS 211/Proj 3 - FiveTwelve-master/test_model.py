"""
Tests for model.py.

Using a DIY 'expect' function rather than the
unittest module. Tests only the model component
of FiveTwelve.
"""
import model
import unittest
import sys


class test_grid_constructor(unittest.TestCase):
    """Grid constructor creates empty 4x4 grid."""

    def test_constructor(self):
        grid = model.Grid()
        rep = grid.as_list()
        self.assertEqual(rep, [[0, 0, 0, 0], [0, 0, 0, 0],
                               [0, 0, 0, 0], [0, 0, 0, 0]])


class test_slide(unittest.TestCase):
    """Sliding left, right, down, up"""

    def expect(self, desc, expected, actual):
        """Equality test with better diagnostics"""
        if actual != expected:
            print("Actual vs. Expected: {}".format(desc))
            for row in range(len(expected)):
                expected_col = expected[row]
                actual_col = actual[row]
                for col in expected_col:
                    print("{:4} ".format(col), end="")
                print(" | ", end="")
                for col in actual_col:
                    print("{:4} ".format(col), end="")
                print()
            print("==============================")
        self.assertEqual(actual, expected)

    def test_left_cascade(self):
        grid = model.Grid()
        grid.set_tiles([[2, 2, 4, 8], [2, 2, 2, 2],
                        [8, 4, 2, 2], [2, 4, 8, 8]])
        grid.left()
        rep = grid.as_list()
        self.expect("Slide left, cascading sums", rep,
                    [[16, 0, 0, 0], [8, 0, 0, 0],
                     [16, 0, 0, 0], [2, 4, 16, 0]])

    def test_right_cascade(self):
        grid = model.Grid()
        grid.set_tiles([[2, 2, 4, 8], [2, 2, 2, 2],
                        [8, 4, 2, 2], [2, 4, 8, 8]])
        grid.right()
        rep = grid.as_list()
        self.expect("Slide right, cascading sums", rep,
                    [[0, 0, 0, 16], [0, 0, 0, 8],
                     [0, 0, 0, 16], [0, 2, 4, 16]])

    def test_left_order(self):
        grid = model.Grid()
        grid.set_tiles([[2, 2, 4, 4], [4, 4, 2, 2],
                        [4, 4, 8, 8], [8, 8, 4, 4]])
        grid.left()
        rep = grid.as_list()
        self.expect("Slide left, collapsing leftmost first", rep,
                    [[8, 4, 0, 0], [8, 4, 0, 0],
                     [16, 8, 0, 0], [16, 8, 0, 0]])

    def test_right_order(self):
        grid = model.Grid()
        grid.set_tiles([[2, 2, 4, 4], [4, 4, 2, 2],
                        [4, 4, 8, 8], [8, 8, 4, 4]])
        grid.right()
        rep = grid.as_list()
        self.expect("Slide right, rightmost collapse first", rep,
                    [[0, 0, 4, 8], [0, 0, 4, 8],
                     [0, 0, 8, 16], [0, 0, 8, 16]])

    def test_down_order(self):
        grid = model.Grid()
        grid.set_tiles([[2, 2, 2, 2],
                        [4, 4, 2, 2],
                        [4, 4, 4, 4],
                        [4, 2, 4, 4]])
        grid.down()
        rep = grid.as_list()
        self.expect("Slide down, working from bottom up", rep,
                    [[0, 0, 0, 0],
                     [2, 2, 0, 0],
                        [4, 8, 4, 4],
                        [8, 2, 8, 8]])

    def test_up_order(self):
        grid = model.Grid()
        grid.set_tiles([[2, 2, 2, 2],
                        [4, 4, 2, 2],
                        [4, 4, 4, 4],
                        [4, 2, 4, 4]])
        grid.up()
        rep = grid.as_list()
        self.expect("Slide up, working from top down", rep,
                    [[2, 2, 8, 8],
                     [8, 8, 4, 4],
                        [4, 2, 0, 0],
                        [0, 0, 0, 0]])


if __name__ == "__main__":
    unittest.main()
