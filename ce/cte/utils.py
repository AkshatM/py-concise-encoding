"""
Utilities to help with structural validation. 
"""

import re
import unicodedata
from zoneinfo import ZoneInfo
from timezonefinder import TimezoneFinder
from datetime import time, datetime, timezone, timedelta

class DataError(Exception):
    def __init__(self, reason, obj, start, end):
        self.reason = reason
        self.object = obj
        self.start = start
        self.end = end
        self.message = rf"Character sequence {self.object[self.start:self.end]} failed parsing: {self.reason}"
        super().__init__(self.message)


WHITESPACE = [
    chr(0x0009),
    chr(0x000A),
    chr(0x000B),
    chr(0x000C),
    chr(0x000D),
    chr(0x0020),
    chr(0x0085),
    chr(0x00A0),
    chr(0x1680),
    chr(0x2000),
    chr(0x2001),
    chr(0x2002),
    chr(0x2003),
    chr(0x2004),
    chr(0x2005),
    chr(0x2006),
    chr(0x2007),
    chr(0x2008),
    chr(0x2009),
    chr(0x2007),
    chr(0x2008),
    chr(0x200A),
    chr(0x2028),
    chr(0x2029),
    chr(0x202F),
    chr(0x205F),
    chr(0x3000),
]

LITERAL_ESCAPE_IDENTIFIER = {
    't': chr(0x0009),
    'n': chr(0x000A),
    'r': chr(0x000D),
    '*': chr(0x002A),
    "/": chr(0x002F),
    "<": chr(0x003C),
    ">": chr(0x003E),
    ">": chr(0x003E),
    "\\": chr(0x005C),
    "|": chr(0x007C),
    "_": chr(0x00A0),
    "-": chr(0x00AD)
}

TERMINATOR_DELIMITER = [chr(0x0020), chr(0x0009), chr(0x000A), chr(0x000D) + chr(0x000A)]


def is_valid_codepoint(c):

    if unicodedata.category(c) in ["Zp", "Zl"]:
        return False

    if unicodedata.category(c).startswith("C"):
        if c not in [chr(0x0009), chr(0x000A), chr(0x000D)]:
            return False

    return True


def validate_float(s, zero_pattern, as_hex=False):
    text = s.replace("_", ".").replace(",", ".")

    try:
        value = float.fromhex(text) if as_hex else float(text)
    except OverflowError:
        raise DataError("Value exceeds IEEE-754 bounds", s, 0, len(s))

    if value == float("inf"):
        raise DataError("Value exceeds IEEE-754 bounds", s, 0, len(s))

    if (value == 0.0 and not re.match(zero_pattern, text)) or value == float("-inf"):
        raise DataError("Value underflows IEEE-754 bounds", s, 0, len(s))

    return value

def validate_string(s: str):
    """
    Given a string:
    1. Ensure no Unicode codepoint in category C, Z1, Zp is presented
       (except for TAB (u+0009), LF (u+000a), and CR (u+000d))
    2. Parse only the following escape sequences:
       https://github.com/kstenerud/concise-encoding/blob/master/cte-specification.md#escape-sequences

    Return a string containing these parsed escape sequences
    """

    verified_s = ""
    index = 0

    while index < len(s):

        if s[index] == "\\":

            index += 1

            if s[index] in LITERAL_ESCAPE_IDENTIFIER:
                verified_s += LITERAL_ESCAPE_IDENTIFIER[s[index]]
                index += 1

            elif s[index] == chr(0x000A) or s[index] == chr(0x000D):

                while index < len(s):
                    if s[index] not in WHITESPACE:
                        break
                    index += 1

            elif s[index].isdigit():

                # no need for bounds check on size because ANTLR only accepts 
                # exact ranges
                size = int(s[index])
                proposed_char = chr(int(s[index + 1 : index + size + 1], 16))

                if not is_valid_codepoint(proposed_char):
                    raise DataError(
                        "Disallowed Unicode codepoint category",
                        s,
                        index - 1,
                        index + size + 1,
                    )

                verified_s += proposed_char
                index += size + 1

            elif s[index] == ".":

                terminator = ''
                index = index + 1

                while index < len(s):

                    if (s[index] in TERMINATOR_DELIMITER):
                        index += 1
                        break

                    if (s[index : index + 2] in TERMINATOR_DELIMITER):
                        index += 2
                        break

                    if s[index] in WHITESPACE or not is_valid_codepoint(s[index]):
                        raise DataError(
                            "Invalid codepoint in verbatim sequence terminator",
                            terminator + s[index],
                            0,
                            len(terminator + s[index]),
                        )

                    terminator += s[index]
                    index += 1

                while index < len(s):
                    if (s[index : index + len(terminator)] == terminator):
                        index += len(terminator)
                        break

                    verified_s += s[index]  # as is
                    index += 1

            continue

        if not is_valid_codepoint(s[index]):
            raise DataError(
                "Disallowed Unicode codepoint category",
                s,
                index,
                index + 1,
            )

        verified_s += s[index]
        index += 1

    return verified_s

def DatetimeKeeper(object):
    """
    A simple wrapper around datetime.datetime that keeps extra information
    not supported by the native datetime module e.g. support for BC dates and
    AD dates larger than 999999.
    """

    def __init__(self):
        pass

# TODO: Refactor to be smaller and more easily maintained. Currently has the benefits
# of being a linear parser, but could use some conciseness.
def validate_time(s: str, utc_offset_expected=False):

    """
    Parse a time string with timezone information. If `utc_offset_expected` is set,
    can be used to parse the time component of a timestamp string as well.

    Why not use datetime.strptime here? Firstly, because %Z is not robust enough to handle
    lat/long types - we need to parse timezone information separately for this. Secondly,
    datetime.strptime requires exact format in advance, whereas CE supports many different 
    types of formats which we cannot predict in advance. It is cleanest to parse and construct
    by hand.
    """

    # unvalidated hour, minute, second, microsecond and tz respectively
    parse_stage = ["", "", "", "", ()]
    index, parse_stage_index = 0, 0

    while index < len(s):

        # hour, minute and second parsing is easy - just grab all
        # characters until a colon comes along
        if parse_stage_index in [0, 1]:

            if s[index] == ":":
                parse_stage_index += 1
            else:
                parse_stage[parse_stage_index] += s[index]

            index += 1
            continue

        if parse_stage_index == 2:

            if s[index] in [".", ",", "/", "+", "-"]:
                parse_stage_index += 1
                continue
            else:
                parse_stage[parse_stage_index] += s[index]
                index += 1
                continue

        # because microsecond is optional, we call into a different parsing
        # parse_stage here. We abort if the start tokens ".", "," are not present,
        # otherwise gather until we encounter a "/", "+", "-".
        if parse_stage_index == 3:

            if s[index] in [".", ","]:
                index += 1
                while index < len(s):
                    if s[index] in ["/", "+", "-"]:
                        parse_stage_index += 1
                        break
                    else:
                        parse_stage[parse_stage_index] += s[index]
                        index += 1
                continue

            else:
                parse_stage_index += 1
                continue

        # time to parse a timezone! Can be a UTC offset, a (lat, long) pair,
        # an (area, location) pair or just an abbreviation. Finish parsing here.
        if parse_stage_index == 4:

            if s[index] in ["+", "-"] and not utc_offset_expected:
                raise DataError("Unexpected UTC offset", s, 0, len(s))
            elif s[index] in ["+", "-"] and utc_offset_expected:
                parse_stage[parse_stage_index] = s[index+1:index+5]
            elif s[index] == "/":
                parse_stage[parse_stage_index] = s[index+1:]

            break

    hour, minute, second, microsecond, tz = parse_stage
    hour, minute, second = int(hour), int(minute), int(second)
    if not 0 <= hour <= 23:
        raise DataError("Hour out of range 0 - 23", s, 0, len(text))
    if not 0 <= minute <= 59:
        raise DataError("Hour out of range 0 - 59", s, 0, len(text))
    if not 0 <= second <= 60:
        raise DataError("Second out of range 0 - 60", s, 0, len(text))

    if microsecond:
        microsecond = int(microsecond)
        if not 0 <= microsecond <= 999999999:
            raise DataError("Microsecond out of range 0 - 999999999", s, 0, len(text))
    else:
        microsecond = 0

    # TODO: This is really messy. We should move this up higher into the parsing stage, return
    # a type and pattern-match based on it. 
    if tz:
        try:
            if tz == "L":
                tz = ZoneInfo(dt.utcnow().astimezone().tzname())
            elif tz == "E":
                tz = ZoneInfo("Etc/UTC")
            elif tz.startswith("F/"):
                tz = ZoneInfo(tz.replace("F/", "Africa/", 1))
            elif tz.startswith("M/"):
                tz = ZoneInfo(tz.replace("M/", "America/", 1))
            elif tz.startswith("N/"):
                tz = ZoneInfo(tz.replace("N/", "Antarctica/", 1))
            elif tz.startswith("R/"):
                tz = ZoneInfo(tz.replace("R/", "Arctic/", 1))
            elif tz.startswith("S/"):
                tz = ZoneInfo(tz.replace("S/", "Asia/", 1))
            elif tz.startswith("T/"):
                tz = ZoneInfo(tz.replace("T/", "Atlantic/", 1))
            elif tz.startswith("U/"):
                tz = ZoneInfo(tz.replace("U/", "Australia/", 1))
            elif tz.startswith("C/"):
                tz = ZoneInfo(tz.replace("C/", "Etc/", 1))
            elif tz.startswith("E/"):
                tz = ZoneInfo(tz.replace("E/", "Europe/", 1))
            elif tz.startswith("I/"):
                tz = ZoneInfo(tz.replace("I/", "Indian/", 1))
            elif tz.startswith("P/"):
                tz = ZoneInfo(tz.replace("P/", "Pacific/", 1))
            elif tz.startswith("+") or (tz.startswith("-") and not tz.contains("/")):
                hours, minutes = int(tz[1:3]), int(tz[3:])
                if tz[0] == "-":
                    hours, minutes = -1*hours, -1*hours
                tz = timezone(timedelta(hours=hours, minutes=minutes))
            elif (tz.startswith("-")) or tz[0].isdigit():
                lat, lng = tz.replace(",", ".").split("/")
                lat, lng = validate_float(lat, r"-?00\.00"), validate_float(
                    lng, r"-?00\.00"
                )
                tzname = TimezoneFinder().timezone_at_land(lng=lng, lat=lat)
                if tzname:
                    tz = ZoneInfo(tzname)
                else:
                    raise DataError(
                        "Could not find timezone for lat/long pair", tz, 0, len(tz)
                    )
            else:
                # last resort
                tz = ZoneInfo(tz)

        except Exception as e:
            raise DataError(f"Unable to validate timezone: {str(e)}", tz, 0, len(tz))
    else:
        tz = ZoneInfo("UTC")

    return time(
        hour=hour, minute=minute, second=second, microsecond=microsecond, tzinfo=tz
    )
