import re
import unicodedata
from zoneinfo import ZoneInfo
from datetime import time
from datetime import datetime
from timezonefinder import TimezoneFinder


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

ENDSEQ_IDENTIFIER = [chr(0x0020), chr(0x0009), chr(0x000A), chr(0x000D) + chr(0x000A)]


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

    index, escape_mode = 0, False
    while index < len(s):

        if escape_mode:

            if s[index] == "t":
                verified_s += chr(0x0009)
            elif s[index] == "n":
                verified_s += chr(0x000A)
            elif s[index] == "r":
                verified_s += chr(0x000D)
            elif s[index] == "*":
                verified_s += chr(0x002A)
            elif s[index] == "/":
                verified_s += chr(0x002F)
            elif s[index] == "<":
                verified_s += chr(0x003C)
            elif s[index] == ">":
                verified_s += chr(0x003E)
            elif s[index] == ">":
                verified_s += chr(0x003E)
            elif s[index] == "\\":
                verified_s += chr(0x005C)
            elif s[index] == "|":
                verified_s += chr(0x007C)
            elif s[index] == "_":
                verified_s += chr(0x00A0)
            elif s[index] == "-":
                verified_s += chr(0x00AD)

            elif s[index] == chr(0x000A) or s[index] == chr(0x000D):

                continuation_range = 0
                while index + continuation_range < len(s):
                    if s[index + continuation_range] in WHITESPACE:
                        continuation_range += 1
                    else:
                        break
                index += continuation_range - 1

            elif s[index].isdigit():

                # no need for bounds check because ANTLR only accepts exact
                # ranges.
                size = int(s[index])
                proposed_char = chr(int(s[index + 1 : index + size + 1], 16))
                if not is_valid_codepoint(proposed_char):
                    raise DataError(
                        "Disallowed Unicode codepoint category",
                        s,
                        index - 1,
                        index + size + 1,
                    )
                else:
                    verified_s += proposed_char
                index += size

            elif s[index] == ".":

                terminator_start = index + 1
                terminator_end = terminator_start

                while terminator_end < len(s):
                    if s[terminator_end] not in WHITESPACE and is_valid_codepoint(
                        s[terminator_end]
                    ):
                        terminator_end += 1
                    else:
                        raise DataError(
                            "Unexpected usage of whitespace or invalid codepoint",
                            s,
                            terminator_start,
                            terminator_end,
                        )

                    if (
                        s[terminator_end] in ENDSEQ_IDENTIFIER
                        or s[terminator_end : terminator_end + 2] in ENDSEQ_IDENTIFIER
                    ):
                        break

                terminator_seq = s[terminator_start:terminator_end]
                terminator_end += 1

                while terminator_end < len(s):
                    if (
                        s[terminator_end : terminator_end + len(terminator_seq)]
                        == terminator_seq
                    ):
                        terminator_end += len(terminator_seq)
                        break
                    else:
                        verified_s += s[terminator_end]  # as is
                        terminator_end += 1

                index = terminator_end - 1

            escape_mode = False

        else:

            if s[index] == "\\":
                escape_mode = True
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


def parse_time(s: str, utc_offset_expected=False):
    """
    Parse a time string with timezone information. If `utc_offset_expected` is set,
    can be used to parse the time component of a timestamp string as well.

    Why not use datetime.strptime here? Firstly, because %Z is not robust enough to handle
    lat/long types - we need to parse timezone information separately for this. Secondly,
    datetime.strptime requires exact formatting, whereas CE supports many different types
    of formats which we cannot predict in advance. It is cleanest to parse and construct
    by hand.
    """

    # unvalidated hour, minute, second, microsecond and tz respectively
    state = ["", "", "", "", ""]
    index, state_index = 0, 0

    while index < len(s):

        # hour, minute and second parsing is easy - just grab all
        # characters until a colon comes along
        if state_index in [0, 1]:

            if s[index] == ":":
                state_index += 1
            else:
                state[state_index] += s[index]

            index += 1
            continue

        if state_index == 2:

            if s[index] in [".", ",", "/", "+", "-"]:
                state_index += 1
                continue
            else:
                state[state_index] += s[index]
                index += 1
                continue

        # because microsecond is optional, we call into a different parsing
        # stage here. We abort if the start tokens ".", "," are not present,
        # otherwise gather until we encounter a "/", "+", "-".
        if state_index == 3:

            if s[index] in [".", ","]:
                microsecond_index = index + 1
                while microsecond_index < len(s):
                    if s[microsecond_index] in ["/", "+", "-"]:
                        state_index += 1
                        break
                    else:
                        state[state_index] += s[microsecond_index]
                        microsecond_index += 1

                index = microsecond_index
                continue

            else:
                state_index += 1
                continue

        # time to parse a timezone!
        if state_index == 4:

            tz_index = index

            if s[tz_index] in ["+", "-"] and not utc_offset_expected:
                raise DataError("Unexpected UTC offset", s, 0, len(index))

            if s[tz_index] == "/":
                # read until the end - validate separately later
                tz_index += 1
                while tz_index < len(s):
                    state[state_index] += s[tz_index]
                    tz_index += 1

            index = tz_index

    hour, minute, second, microsecond, tz = state
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
            elif tz.startswith("-") or tz[0].isdigit():
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
