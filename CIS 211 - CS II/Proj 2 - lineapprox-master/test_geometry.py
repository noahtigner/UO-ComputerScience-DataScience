"""
Tests for polyline simplification. 

"""

import unittest
import geometry
import logging

class Test_Distance(unittest.TestCase):
    """Simple unit tests of distance calculation"""

    def test_from_floor(self):
        """Segment along horizontal axis"""
        self.assertEqual(
            geometry.deviation((0,0),(100,0),(50,50)), 50)

    def test_from_level(self):
        """Segment from horizontal line, not at zero"""
        self.assertEqual(
            geometry.deviation((100,100),(200,100),(150,300)), 200)

    def test_from_vertical(self):
        """Segment from vertical line"""
        self.assertEqual(
            geometry.deviation((100,100),(100,200),(150,150)), 50)
        
    
class TestSimplify(unittest.TestCase):
    """Simple unit tests for D-P polyline approximation"""

    def test_three_straight(self):
        """Should remove the intermediate point"""
        geometry.log.setLevel(logging.INFO)
        path = geometry.PolyLine([(0,0), (50,50), (100,100)])
        path.simplify(25)
        self.assertEqual(path.approx, [(0,0), (100,100)])

    def test_straight_simplify(self):
        """Should remove all intermediate points"""
        geometry.log.setLevel(logging.INFO)
        points = [(0,0), (20,20), (30,30), (40,40), (50,50),
                      (60,60), (70,70), (80,80), (100,100) ]
            
        path = geometry.PolyLine(points)
        path.simplify(25)
        self.assertEqual(path.approx, [(0,0), (100,100)])

    def test_ridge(self):
        """Simpler than zigzag ... one ridge"""
        geometry.log.setLevel(logging.INFO)
        points = [(0,0), (50,50), (100,100),
                  (150,50), (200,0)]
        path = geometry.PolyLine(points)
        path.simplify(20)
        self.assertEqual(path.approx,
           [(0,0), (100,100), (200, 0)])

    def test_zigzag_simplify(self):
        geometry.log.setLevel(logging.INFO)    
        points = [ (0,0), (50,100), (100,200), (150,100), (200,0),
                       (250,100), (300,200), (350,100), (400,0),
                       (450,100), (500,200), (550,100), (600,0) ]
        path = geometry.PolyLine(points)
        path.simplify(75)
        self.assertEqual(path.approx, [(0,0), (100,200),
                                          (200,0), (300,200),
                                          (400,0), (500,200),
                                          (600,0)])




if __name__ == "__main__":
    unittest.main()
