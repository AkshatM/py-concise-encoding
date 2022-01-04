import re
from calendar import Calendar
from datetime import datetime
from zoneinfo import ZoneInfo
from timezonefinder import TimezoneFinder
from ce.primitive_types import validated_string, validated_float

class Rid(object):
    def __init__(self, s: str, **kwargs):
        self.rid = validated_string(s, **kwargs)

    def __eq__(self, other):

        if not isinstance(other, Rid):
            return False

        return self.rid == other.rid

    def __hash__(self, other):
        return hash(self.rid)

    def __repr__(self):
        return self.rid


Coordinates = tuple[float, float]

# TODO: Make attrs immutable
class Time(object):

    AREA_ABBREVIATIONS = {
        "F": "Africa",
        "M": "America",
        "N": "Antarctica",
        "R": "Arctic",
        "S": "Asia",
        "T": "Atlantic",
        "U": "Australia",
        "C": "Etc",
        "E": "Europe",
        "I": "Indian",
        "P": "Pacific",
    }

    @classmethod
    def validated_hour(_, hour: int | str):
        if isinstance(hour, str):
            hour = int(hour)

        if isinstance(hour, int):
            if not 0 <= hour <= 23:
                raise Exception("Hour is not in range 0 - 23")
            return hour

        raise Exception("Hour is not in desired type")

    @classmethod
    def validated_minute(_, minute: int | str):
        if isinstance(minute, str):
            minute = int(minute)

        if isinstance(minute, int):
            if not 0 <= minute <= 59:
                raise Exception("Hour is not in range 0 - 59")
            return minute

        raise Exception("Hour is not in desired type")

    @classmethod
    def validated_second(_, second: int | str):
        if isinstance(second, str):
            second = int(second)

        if isinstance(second, int):
            if not 0 <= second <= 60:
                raise Exception("Second is not in range 0 - 60")
            return second

        raise Exception("Second is not in desired type")

    @classmethod
    def validated_nanosecond(_, nanosecond: int | str | None):

        if nanosecond is None:
            return None

        if isinstance(nanosecond, str):
            if nanosecond == '':
                return None
            nanosecond = int(nanosecond)

        if isinstance(nanosecond, int):
            if not 0 <= nanosecond <= 999999999:
                raise Exception("Nanosecond is not in range 0 - 999999999")
            return nanosecond

        raise Exception("Nanosecond is not in desired type")

    @classmethod
    def validated_timezone(cls, tzrepr: Coordinates | str | None):

        if tzrepr is None:
            return "UTC"

        if isinstance(tzrepr, tuple):
            if len(tzrepr) == 2 and all(isinstance(x, float) for x in tzrepr):
                lat, lng = tzrepr
                return TimezoneFinder().timezone_at_land(lng=lng, lat=lat)

            raise Exception("Got invalid tuple as arguments")

        if isinstance(tzrepr, str):

            if tzrepr == "":
                return "UTC"

            if tzrepr == "L":
                return datetime.utcnow().astimezone().tzname()

            if tzrepr == "E":
                return "Etc/UTC"

            expansion_match = re.match(r"^([FMNRSTUCEIP])/(.+)", tzrepr)
            if expansion_match:
                area, locale = expansion_match.groups()
                expansion = cls.AREA_ABBREVIATIONS[area]
                return str(ZoneInfo(f"{expansion}/{locale}"))

            utc_offset_match = re.match(r"[+|-](\d{2})(\d{2})", tzrepr)
            if utc_offset_match:
                hour, minute = utc_offset_match.groups()
                if tzrepr.startswith("-"):
                    hour, minute = -1 * hour, -1 * hour
                # returns strings that resemble UTC[+|-]\d{2}:\d{2}
                return str(timezone(timedelta(hours=hours, minutes=minutes)))

            lat_lng_pattern = r"^(-?\d{2}\.\d{2})/(-?\d{2}\.\d{2})$"
            lat_lng_match = re.match(lat_lng_pattern, tzrepr)
            if lat_lng_match:
                lat, lng = map(validated_float, lat_lng_match.groups())
                return TimezoneFinder().timezone_at_land(lng=lng, lat=lat)

            # last resort
            return str(ZoneInfo(tzrepr))

        raise Exception("Timezone is not of desired type")

    def __init__(self, hour, minute, second, nanosecond, tzname):
        self.hour = self.validated_hour(hour)
        self.minute = self.validated_minute(minute)
        self.second = self.validated_second(second)
        self.nanosecond = self.validated_nanosecond(nanosecond)
        self.tzname = self.validated_timezone(tzname)
        self.is_utc_offset = (
            re.match(r"UTC[+|-]\d{2}:\d{2}", self.tzname)
        ) is not None

    def __eq__(self, other):

        if not isinstance(other, Time):
            return False

        return all(
            getattr(self, attr) == getattr(other, attr)
            for attr in ["hour", "minute", "second", "nanosecond", "tzname"]
        )

    def __hash__(self, other):
        return (hour, minute, second, nanosecond, timezone)

    def __repr__(self):
        attributes = [str(getattr(self, a)) for a in ["hour", "minute", "second", "nanosecond", "tzname", "is_utc_offset"]]
        return f"Time({','.join(attributes)})"

    @classmethod
    def from_string(_, s: str, utc_offset_expected=False):

        """
        Parse a time string with timezone information. If `utc_offset_expected` is set,
        can be used to parse the time component of a timestamp string as well.
        """

        if s == '':
            return None


        # Why not use datetime.strptime here? Firstly, because %Z is not robust enough to handle
        # lat/long types - we need to parse timezone information separately for this. Secondly,
        # datetime.strptime requires exact format in advance, whereas CE supports many different
        # types of formats which we cannot predict in advance. It is cleanest to parse and construct
        # by hand. Might consider refactoring to require something less verbose than a linear scan,
        # but it works for now.

        # unvalidated hour, minute, second, nanosecond and tz respectively

        pattern = r'(\d{2}):(\d{2}):(\d{2})'
        parse_state = ["", "", "", "", ""]
        index, parse_stage = 0, 0

        while index < len(s):

            # hour, minute parsing is easy - just grab all
            # characters until a colon comes along
            if parse_stage in [0, 1]:

                if s[index] == ":":
                    parse_stage += 1
                else:
                    parse_state[parse_stage] += s[index]

                index += 1
                continue

            # parsing a second is only slightly complicated by the presence of different
            # stopping characters
            if parse_stage == 2:

                if s[index] in [".", ",", "/", "+", "-"]:
                    parse_stage += 1
                    continue
                else:
                    parse_state[parse_stage] += s[index]
                    index += 1
                    continue

            # because nanosecond is optional, we abort if the start tokens ".", "," are not present,
            # otherwise gather until we encounter a "/", "+", "-".
            if parse_stage == 3:

                if s[index] in [".", ","]:
                    index += 1
                    while index < len(s):
                        if s[index] in ["/", "+", "-"]:
                            parse_stage += 1
                            break
                        else:
                            parse_state[parse_stage] += s[index]
                            index += 1
                    continue

                else:
                    parse_stage += 1
                    continue

            # time to parse a timezone!
            if parse_stage == 4:

                if s[index] in ["+", "-"] and not utc_offset_expected:
                    raise Exception("Unexpected UTC offset")
                elif s[index] in ["+", "-"] and utc_offset_expected:
                    parse_state[parse_stage] = s[index + 1 : index + 5]
                elif s[index] == "/":
                    parse_state[parse_stage] = s[index + 1 :]

                break

        hour, minute, second, nanosecond, tzname = parse_state
        return Time(
            hour=hour,
            minute=minute,
            second=second,
            nanosecond=nanosecond,
            tzname=tzname,
        )

class Timestamp(object):

    @classmethod
    def validated_year(_, year: int | str):
        if isinstance(year, str):
            year = int(year)

        if isinstance(year, int):
            if year == 0:
                raise Exception("Year cannot be zero")
            return year

        raise Exception("Year is not in desired type")

    @classmethod
    def validated_month(_, month: int | str):
        if isinstance(month, str):
            month = int(month)

        if isinstance(month, int):
            if not 1 <= month <= 12:
                raise Exception("Month is not in range 1 - 12")
            return month

        raise Exception("Month is not in desired type")

    @classmethod
    def validated_day(_, year: int|str, month: int|str, day: int | str):

        if isinstance(month, str):
            month = self.validated_month(month)

        if isinstance(year, str):
            year = self.validated_year(year)

        if isinstance(day, str):
            day = int(day)

        if isinstance(day, int):
            if day < 0 or day not in Calendar().itermonthdays(year, month):
                raise Exception("Day is not valid for given year and month")
            return day

        raise Exception("Day is not in desired type")

    def __init__(self, year, month, day, time=None):
        self.year = self.validated_year(year)
        self.month = self.validated_month(month)
        self.day = self.validated_day(self.year, self.month, day)
        if isinstance(time, Time) or time is None:
            self.time = time
        elif isinstance(time, str):
            self.time = Time.from_string(time)
        else:
            raise Exception("Time is of unexpected type")

    def __eq__(self, other):

        if not isinstance(other, Timestamp):
            return False

        return all(
            getattr(self, attr) == getattr(other, attr)
            for attr in ["year", "month", "day", "time"]
        )

    def __hash__(self, other):
        return (year, month, day, time)

    def __repr__(self):
        attributes = [str(getattr(self, a)) for a in ["year", "month", "day", "time"]]
        return f"Timestamp({','.join(attributes)})"


    @classmethod
    def from_string(_, s: str):
        match = re.fullmatch(r'(-?\d+)-(\d{2})-(\d{2})(.*)', s).groups()
        year, month, day, time = match
        return Timestamp(year, month, day,time=time.lstrip('/') if time else None)