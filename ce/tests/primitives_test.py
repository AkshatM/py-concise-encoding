import os
import unittest
import ce.cte as cte
from datetime import time
from zoneinfo import ZoneInfo
from ce.cte.utils import DataError


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
        self.assertEqual(cte.load("c1 0.0"), 0.0)

    def test_decimal_float_case1(self):
        self.assertEqual(cte.load("c1 0.1"), 0.1)

    def test_decimal_float_case2(self):
        self.assertEqual(cte.load("c1 -0.1"), -0.1)

    def test_decimal_float_case3(self):
        self.assertEqual(cte.load("c1 0,1"), 0.1)

    def test_decimal_float_case4(self):
        self.assertEqual(cte.load("c1 -0,1"), -0.1)

    def test_decimal_float_case5(self):
        self.assertEqual(cte.load("c1 1e1"), 10)

    def test_decimal_float_case6(self):
        self.assertEqual(cte.load("c1 -1e1"), -10)

    def test_decimal_float_case7(self):
        self.assertEqual(cte.load("c1 1.1e1"), 11)

    def test_decimal_float_case8(self):
        self.assertEqual(cte.load("c1 -1.1e1"), -11)

    def test_decimal_float_case9(self):
        self.assertEqual(cte.load("c1 1,1e1"), 11)

    def test_decimal_float_case10(self):
        self.assertEqual(cte.load("c1 -1,1e1"), -11)

    def test_hexadecimal_float_zero(self):
        self.assertEqual(cte.load("c1 0.0p+0"), 0.0)

    def test_hexadecimal_float_case1(self):
        self.assertEqual(cte.load("c1 0x0.1p0"), 0.0625)

    def test_hexadecimal_float_case2(self):
        self.assertEqual(cte.load("c1 0xaf.b7p+0"), 175.71484375)

    def test_hexadecimal_float_case3(self):
        self.assertEqual(cte.load("c1 0xaf.b7p+2"), 702.859375)

    def test_hexadecimal_float_case4(self):
        self.assertEqual(cte.load("c1 0xaf.b7p-2"), 43.9287109375)

    def test_hexadecimal_float_case5(self):
        self.assertEqual(cte.load("c1 0xaf.b7p3"), 1405.71875)

    def test_decimal_float_overflow(self):
        with self.assertRaises(DataError):
            cte.load("c1 1e20000")

    def test_decimal_float_underflow(self):
        with self.assertRaises(DataError):
            cte.load("c1 1e-20000")

    def test_hexadecimal_float_overflow(self):
        with self.assertRaises(DataError):
            cte.load("c1 0x1p1024")

    def test_hexadecimal_float_underflow(self):
        with self.assertRaises(DataError):
            cte.load("c1 0x1p-102400")

    def test_nan(self):
        self.assertTrue(cte.load("c1 nan").is_nan())

    def test_inf(self):
        self.assertEqual(cte.load("c1 inf"), float("inf"))

    def test_negative_inf(self):
        self.assertEqual(cte.load("c1 -inf"), float("-inf"))

    def test_snan(self):
        self.assertTrue(cte.load("c1 snan").is_snan())

    def test_rid(self):
        self.assertEqual(
            cte.load("""c1 @\"http://x.y.z?quote=\""""), "http://x.y.z?quote="
        )

    def test_pathological_rid(self):

        filename = os.path.join(
            os.path.dirname(__file__), "examples/pathological_string.cte"
        )
        with open(filename, "r") as f:
            test = f.read()
            self.assertEqual(cte.load(test), "ab\u000a\u0009\u0123cde   \\.f\u0009g")

    def test_simple_time(self):

        self.assertEqual(
            cte.load("""c1 21:05:04"""), time(21, 5, 4, 0, ZoneInfo("UTC"))
        )

    def test_simple_time_with_microsecond(self):

        self.assertEqual(
            cte.load("""c1 21:05:04.4444"""), time(21, 5, 4, 4444, ZoneInfo("UTC"))
        )

    def test_simple_time_with_microsecond_and_timezone(self):

        self.assertEqual(
            cte.load("""c1 21:05:04.444/E"""), time(21, 5, 4, 444, ZoneInfo("Etc/UTC"))
        )

    def test_simple_time_with_lat_and_long(self):

        self.assertEqual(
            cte.load("""c1 21:05:04.444/51.34/71.52"""),
            time(21, 5, 4, 444, ZoneInfo("Asia/Almaty")),
        )
