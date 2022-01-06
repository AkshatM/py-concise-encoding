"""
All basic numeric and string types and their associated handling. 
"""

import re
import unicodedata
from enum import Enum
from zoneinfo import ZoneInfo
from decimal import Decimal
from timezonefinder import TimezoneFinder

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
    "t": chr(0x0009),
    "n": chr(0x000A),
    "r": chr(0x000D),
    "*": chr(0x002A),
    "/": chr(0x002F),
    "<": chr(0x003C),
    ">": chr(0x003E),
    ">": chr(0x003E),
    "\\": chr(0x005C),
    "|": chr(0x007C),
    "_": chr(0x00A0),
    "-": chr(0x00AD),
}

TERMINATOR_DELIMITER = [
    chr(0x0020),
    chr(0x0009),
    chr(0x000A),
    chr(0x000D) + chr(0x000A),
]


def is_valid_codepoint(c):

    if unicodedata.category(c) in ["Zp", "Zl"]:
        return False

    if unicodedata.category(c).startswith("C"):
        if c not in [chr(0x0009), chr(0x000A), chr(0x000D)]:
            return False

    return True

class BinaryFloat(object):

    def __init__(self, f: str):
        self.float = self.__validate_binary_float(f)
        self.as_decimal = Decimal(float.fromhex(self.float))

    def __validate_binary_float(self, s: str):
        """
        Take a representation of a binary float and cast it to a float, verifying
        if the given float is within the IEE-754 range.
        """

        # In Python, floats smaller than the IEE-754 range get silently cast
        # to 0.0. This is a violation of the CE spec, which requires a data
        # error in such cases. Hence, we artificially detect it
        # by checking if the text "looks like" a pattern that should not have been
        # cast to zero but was, which is doable because there are only finitely
        # many such patterns.


        text = s.replace("_", "").replace(",", ".")
        zero_pattern = r"-?0x0+(?P<dot>\.)?(?(dot)0+)(?P<exp>p)?(?(exp).*)"

        try:
            value = float.fromhex(text)
        except OverflowError:
            raise Exception(f"Value {s} exceeds IEEE-754 bounds")

        if (value == 0.0 and re.match(zero_pattern, text) is None):
            raise Exception(f"Value {s} underflows IEEE-754 bounds")

        return text

    def __eq__(self, other):

        if isinstance(other, BinaryFloat):
            return self.as_decimal.__eq__(other.as_decimal)

    def __hash__(self):
        return self.as_decimal.__hash__()

    def __repr__(self):
        return f'BinaryFloat({self.float}={self.as_decimal})'



def validated_string(s: str, allow_NULs=False):
    """
    Given a string:
    1. Ensure no Unicode codepoint in category C, Z1, Zp is presented
       (except for TAB (u+0009), LF (u+000a), and CR (u+000d))
    2. Parse only the following escape sequences:
       https://github.com/kstenerud/concise-encoding/blob/master/cte-specification.md#escape-sequences
    3. Throw an error for any NUL character found, unless NUL support is enabled.

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
                    raise Exception(
                        "Disallowed Unicode codepoint category",
                        s,
                        index - 1,
                        index + size + 1,
                    )

                verified_s += proposed_char
                index += size + 1

            elif s[index] == ".":

                terminator = ""
                index = index + 1

                while index < len(s):

                    if s[index] in TERMINATOR_DELIMITER:
                        index += 1
                        break

                    if s[index : index + 2] in TERMINATOR_DELIMITER:
                        index += 2
                        break

                    if s[index] in WHITESPACE or not is_valid_codepoint(s[index]):
                        raise Exception(
                            "Invalid codepoint in verbatim sequence terminator",
                            terminator + s[index],
                            0,
                            len(terminator + s[index]),
                        )

                    terminator += s[index]
                    index += 1

                while index < len(s):
                    if s[index : index + len(terminator)] == terminator:
                        index += len(terminator)
                        break

                    verified_s += s[index]  # as is
                    index += 1

            continue

        if not is_valid_codepoint(s[index]):
            raise Exception(
                "Disallowed Unicode codepoint category",
                s,
                index,
                index + 1,
            )

        if s[index] == chr(0x0000) and not allow_NULs:
            raise Exception(
                "Disallowed NUL encounted",
                s,
                index,
                index + 1,
            )

        verified_s += s[index]
        index += 1

    return verified_s
