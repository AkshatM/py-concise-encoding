import os
import unittest
import ce.cte as cte
from datetime import time
from decimal import Decimal
from zoneinfo import ZoneInfo
from ce.complex_types import Rid
from ce.primitive_types import BinaryFloat


class PrimitivesTestCase(unittest.TestCase):
    def test_invalid_version(self):
        with self.assertRaises(Exception):
            cte.load("c2 false")

    def test_bool(self):
        self.assertTrue(cte.load("c1 true"))

    def test_false(self):
        self.assertFalse(cte.load("c1 false"))

    def test_pint_dec(self):
        self.assertEqual(cte.load("c1 5"), 5)

    def test_nint_dec(self):
        self.assertEqual(cte.load("c1 -5"), -5)

    def test_pint_bin(self):
        self.assertEqual(cte.load("c1 0b1"), 1)

    def test_nint_bin(self):
        self.assertEqual(cte.load("c1 -0b1"), -1)

    def test_pint_oct(self):
        self.assertEqual(cte.load("c1 0o1"), 1)

    def test_nint_oct(self):
        self.assertEqual(cte.load("c1 -0o1"), -1)

    def test_pint_hex(self):
        self.assertEqual(cte.load("c1 0x1"), 1)

    def test_nint_hex(self):
        self.assertEqual(cte.load("c1 -0x1"), -1)

    def test_decimal_float_zero(self):
        self.assertEqual(cte.load("c1 0.0"), Decimal("0.0"))

    def test_decimal_float_case1(self):
        self.assertEqual(cte.load("c1 0.1"), Decimal("0.1"))

    def test_decimal_float_case2(self):
        self.assertEqual(cte.load("c1 -0.1"), Decimal("-0.1"))

    def test_decimal_float_case3(self):
        self.assertEqual(cte.load("c1 0,1"), Decimal("0.1"))

    def test_decimal_float_case4(self):
        self.assertEqual(cte.load("c1 -0,1"), Decimal("-0.1"))

    def test_decimal_float_case5(self):
        self.assertEqual(cte.load("c1 1e1"), Decimal('1E+1'))

    def test_decimal_float_case6(self):
        self.assertEqual(cte.load("c1 -1e1"), Decimal('-1E+1'))

    def test_decimal_float_case7(self):
        self.assertEqual(cte.load("c1 1.1e1"), Decimal('1.1E+1'))

    def test_decimal_float_case8(self):
        self.assertEqual(cte.load("c1 -1.1e1"), Decimal('-1.1E+1'))

    def test_decimal_float_case9(self):
        self.assertEqual(cte.load("c1 1,1e1"), Decimal('1.1E+1'))

    def test_decimal_float_case10(self):
        self.assertEqual(cte.load("c1 -1,1e1"), Decimal('-1.1E+1'))

    def test_hexadecimal_float_zero(self):
        self.assertEqual(cte.load("c1 0x0.0p+0"), BinaryFloat('0x0.0p+0'))

    def test_hexadecimal_float_case1(self):
        self.assertEqual(cte.load("c1 0x0.1p0"), BinaryFloat("0x0.1p0"))

    def test_hexadecimal_float_case2(self):
        self.assertEqual(cte.load("c1 0xaf.b7p+0"), BinaryFloat("0xaf.b7p+0"))

    def test_hexadecimal_float_case3(self):
        self.assertEqual(cte.load("c1 0xaf.b7p+2"), BinaryFloat("0xaf.b7p+2"))

    def test_hexadecimal_float_case4(self):
        self.assertEqual(cte.load("c1 0xaf.b7p-2"), BinaryFloat("0xaf.b7p-2"))

    def test_hexadecimal_float_case5(self):
        self.assertEqual(cte.load("c1 0xaf.b7p3"), BinaryFloat("0xaf.b7p3"))

    def test_decimal_float_overflow(self):
        self.assertEqual(cte.load("c1 1e20000"), Decimal("1e20000"))

    def test_decimal_float_underflow(self):
        self.assertEqual(cte.load("c1 -1e20000"), Decimal("-1e20000"))

    def test_hexadecimal_float_overflow(self):
        with self.assertRaises(Exception):
            cte.load("c1 0x1p1024")

    def test_hexadecimal_float_underflow(self):
        with self.assertRaises(Exception):
            cte.load("c1 0x1p-102400")

    def test_nan(self):
        self.assertTrue(cte.load("c1 nan").is_nan())

    def test_inf(self):
        self.assertEqual(cte.load("c1 inf"), Decimal("inf"))

    def test_negative_inf(self):
        self.assertEqual(cte.load("c1 -inf"), Decimal("-inf"))

    def test_snan(self):
        self.assertTrue(cte.load("c1 snan").is_snan())
