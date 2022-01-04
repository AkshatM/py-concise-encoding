import unittest
import ce.cte as cte
from ce.complex_types import Time, Timestamp


class DatesAndTimeTestCase(unittest.TestCase):
    def test_simple_time(self):

        self.assertEqual(cte.load("""c1 21:05:04"""), Time(21, 5, 4, None, "UTC"))

    def test_simple_time_with_microsecond(self):

        self.assertEqual(cte.load("""c1 21:05:04.4444"""), Time(21, 5, 4, 4444, "UTC"))

    def test_simple_time_with_microsecond_and_timezone(self):

        self.assertEqual(
            cte.load("""c1 21:05:04.444/E"""), Time(21, 5, 4, 444, "Etc/UTC")
        )

    def test_simple_time_with_area_location_tz(self):

        self.assertEqual(
            cte.load("""c1 21:05:04.444/Asia/Almaty"""),
            Time(21, 5, 4, 444, "Asia/Almaty"),
        )

    def test_simple_time_with_abbreviated_area_location_tz(self):

        self.assertEqual(
            cte.load("""c1 21:05:04.444/S/Almaty"""),
            Time(21, 5, 4, 444, "Asia/Almaty"),
        )

    def test_simple_time_with_lat_and_long(self):

        self.assertEqual(
            cte.load("""c1 21:05:04.444/51.34/71.52"""),
            Time(21, 5, 4, 444, "Asia/Almaty"),
        )

    def test_simple_date(self):

        self.assertEqual(
            cte.load("""c1 1992-03-04"""),
            Timestamp(1992, 3, 4, None),
        )

    def test_negative_date(self):

        self.assertEqual(
            cte.load("""c1 -1992-03-04"""),
            Timestamp(-1992, 3, 4, None),
        )

    def test_invalid_simple_date(self):

        with self.assertRaises(Exception):
            cte.load("""c1 0-03-04""")

    def test_timestamp(self):

        self.assertEqual(
            cte.load("""c1 1992-03-04/21:05:04"""),
            Timestamp(1992, 3, 4, Time(21, 5, 4, None, None)),
        )

    def test_complex_timestamp(self):

        self.assertEqual(
            cte.load("""c1 1992-03-04/21:05:04.444/51.34/71.52"""),
            Timestamp(1992, 3, 4, Time(21, 5, 4, 444, "Asia/Almaty")),
        )
