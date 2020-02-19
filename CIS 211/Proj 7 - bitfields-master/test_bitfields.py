"""
Tests for bitfield.py
"""

import unittest
from bitfield import BitField


class TestExpr(unittest.TestCase):

    def test_low_order(self):
        low_4 = BitField(0,3)
        # A value that fits snugly in the first 4 bits
        self.assertEqual(low_4.insert(13,0), 13)
        # A value that doesn't fit; some high bits lost
        self.assertEqual(low_4.insert(21,0), 5)
        # Extract unsigned
        self.assertEqual(low_4.extract(15), 15)
        # Or convert negative numbers 
        self.assertEqual(low_4.extract_signed(15), -1)
        # Doesn't clobber other bits
        higher = 15 << 4
        self.assertEqual(low_4.insert(13,higher), 13 + higher)
        # Extraction is masked
        packed = low_4.insert(13,higher)
        self.assertEqual(low_4.extract(packed),13)

    def test_middle_bits(self):
        mid_4 = BitField(4,7)
        # A value that fits snugly in4 bits
        self.assertEqual(mid_4.insert(13,0), 13 << 4)
        # A value that doesn't fit; some high bits lost
        self.assertEqual(mid_4.insert(21,0), 5 << 4)
        # Extract unsigned
        self.assertEqual(mid_4.extract(15 << 4), 15)
        # Or convert negative numbers 
        self.assertEqual(mid_4.extract_signed(15 << 4), -1)

    def test_invert(self):
        lowpart = BitField(0,3)
        midpart = BitField(4,6)
        highpart = BitField(7,9)
        for v in range(8):
            packed = 0
            packed = lowpart.insert(v,packed)
            packed = midpart.insert(v,packed)
            packed = highpart.insert(v,packed)
            self.assertEqual(lowpart.extract(packed), v)
            self.assertEqual(midpart.extract(packed), v)
            self.assertEqual(highpart.extract(packed), v)

if __name__ == '__main__':
    unittest.main()

