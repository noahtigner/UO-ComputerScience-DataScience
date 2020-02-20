"""
Tests for expr.py,
  (excludes parsing)

"""

import unittest
import expr
from rpn_parse import parse
import logging


class TestExpr(unittest.TestCase):

    def test_const(self):
        seven = expr.Const(7)
        self.assertEqual(repr(seven), 'Const(7)')
        self.assertEqual(str(seven), '7')
        self.assertEqual(seven.eval(), expr.Const(7))

    def test_plus(self):
        eight = expr.Const(8)
        nine = expr.Const(9)
        x = expr.Var('x')
        y = expr.Var('y')
        self.assertEqual(expr.Plus(x, y), expr.Plus(x, y))
        self.assertEqual(expr.Plus(eight, nine).eval(), expr.Const(17))
        self.assertEqual(expr.Plus(eight, expr.Plus(nine, eight)).eval(),
                         expr.Const(25))
        self.assertEqual(repr(expr.Plus(eight, nine)),
                         "Plus(Const(8),Const(9))")
        self.assertEqual(str(expr.Plus(eight, nine)), "(8 + 9)")

    def test_minus(self):
        eight = expr.Const(8)
        nine = expr.Const(9)
        x = expr.Var('x')
        y = expr.Var('y')
        self.assertEqual(expr.Minus(x, y), expr.Minus(x, y))
        self.assertEqual(expr.Minus(nine, eight).eval(), expr.Const(1))
        self.assertEqual(expr.Minus(eight, expr.Minus(nine, eight)).eval(),
                         expr.Const(7))
        self.assertEqual(repr(expr.Minus(eight, nine)),
                         "Minus(Const(8),Const(9))")
        self.assertEqual(str(expr.Minus(eight, nine)), "(8 - 9)")

    def test_times(self):
        three = expr.Const(3)
        four = expr.Const(4)
        x = expr.Var('x')
        y = expr.Var('y')
        self.assertEqual(expr.Times(x, y), expr.Times(x, y))
        self.assertNotEqual(expr.Times(x, y), expr.Plus(x, y))
        self.assertEqual(expr.Times(three, four).eval(), expr.Const(12))
        self.assertEqual(expr.Times(three, expr.Times(three, four)).eval(),
                         expr.Const(36))

    def test_div(self):
        three = expr.Const(3)
        nine = expr.Const(9)
        x = expr.Var('x')
        y = expr.Var('y')
        self.assertEqual(expr.Div(x, y), expr.Div(x, y))
        self.assertNotEqual(expr.Div(x, y), expr.Times(x, y))
        self.assertEqual(expr.Div(nine, three).eval(), expr.Const(3))
        self.assertEqual(expr.Div(nine, expr.Times(three, three)).eval(),
                         expr.Const(1))

    def test_assign(self):
        """Assignments:  Assign(var, exp) """
        x = expr.Var('x')
        y = expr.Var('y')
        x_exp = expr.Assign(x, expr.Plus(y, expr.Const(9))).eval()
        # x == y + 9
        y_val = expr.Assign(y, expr.Const(3)).eval()
        # y == 3
        # y==3 => (y + 9) + 4 -> 12 + 4 -> 16
        # print("x ({}) = {}".format(x, x.eval()))
        # print("y ({}) = {}".format(y, y.eval()))
        result = expr.Plus(x, expr.Const(4)).eval()
        # print("x + 4 = {}".format(result))
        self.assertEqual(result, expr.Const(16))
        # Change value of y, and x should change also
        y_val = expr.Assign(y, expr.Const(6)).eval()
        self.assertEqual(y_val, expr.Const(6))
        self.assertNotEqual(expr.Plus(x, expr.Const(4)), expr.Const(16))
        # y==6 => (y + 9) + 4 -> 19
        self.assertEqual(expr.Plus(x, expr.Const(4)).eval(),
                         expr.Const(19))


if __name__ == '__main__':
    unittest.main()
