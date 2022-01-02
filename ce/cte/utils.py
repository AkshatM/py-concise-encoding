import unicodedata

WHITESPACE = [
    chr(0x0009), 
    chr(0x000a), 
    chr(0x000b),
    chr(0x000c),
    chr(0x000d), 
    chr(0x0020),
    chr(0x0085),
    chr(0x00a0),
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
    chr(0x200a),
    chr(0x2028),
    chr(0x2029),
    chr(0x202f),
    chr(0x205f),
    chr(0x3000)
]

ENDSEQ_IDENTIFIER = [
    chr(0x0020),
    chr(0x0009),
    chr(0x000a),
    chr(0x000d) + chr(0x000a)
]

def is_valid_codepoint(c):

    if unicodedata.category(c) in ["Zp", "Zl"]:
        return False

    if unicodedata.category(c).startswith("C"):
        if c not in [chr(0x0009), chr(0x000a), chr(0x000d)]:
            return False

    return True

def validate_string(s: str):
    """
    1. Ensure no Unicode codepoint in category C, Z1, Zp is presented
       (except for TAB (u+0009), LF (u+000a), and CR (u+000d))
    2. Parse only the following escape sequences: 
       https://github.com/kstenerud/concise-encoding/blob/master/cte-specification.md#escape-sequences
    """

    verified_s = ""

    index, escape_mode = 0, False
    while index < len(s):

        if escape_mode:

            if s[index] == 't':
                verified_s += chr(0x0009)
            elif s[index] == 'n':
                verified_s += chr(0x000a)
            elif s[index] == 'r':
                verified_s += chr(0x000d)
            elif s[index] == '*':
                verified_s += chr(0x002a)
            elif s[index] == '/':
                verified_s += chr(0x002f)
            elif s[index] == '<':
                verified_s += chr(0x003c)
            elif s[index] == '>':
                verified_s += chr(0x003e)
            elif s[index] == '>':
                verified_s += chr(0x003e)
            elif s[index] == '\\':
                verified_s += chr(0x005c)
            elif s[index] == '|':
                verified_s += chr(0x007c)
            elif s[index] == '_':
                verified_s += chr(0x00a0)
            elif s[index] == '-':
                verified_s += chr(0x00ad)

            elif s[index] == chr(0x000a) or s[index] == chr(0x000d):

                continuation_range = 0
                while index + continuation_range < len(s):
                    if s[index + continuation_range] in WHITESPACE:
                        continuation_range += 1
                    else:
                        break
                index += continuation_range - 1

            elif s[index].isdigit():

                # no need for bounds check because ANTLR only accepts certain
                # ranges.
                size = int(s[index])
                proposed_char = chr(int(s[index + 1: index + size + 1], 16))
                if not is_valid_codepoint(proposed_char):
                    raise UnicodeDecodeError('utf-8', s, index - 1, index + size + 1, 'Disallowed Unicode codepoint category')
                else:
                    verified_s += proposed_char
                index += size

            elif s[index] == ".":

                terminator_start = index + 1
                terminator_end = terminator_start

                while terminator_end < len(s):
                    if s[terminator_end] not in WHITESPACE and is_valid_codepoint(s[terminator_end]):
                        terminator_end += 1
                    else: 
                        raise UnicodeDecodeError('utf-8', s, terminator_start, terminator_end, 'Unexpected usage of whitespace or invalid codepoint')

                    if s[terminator_end] in ENDSEQ_IDENTIFIER or s[terminator_end: terminator_end+2] in ENDSEQ_IDENTIFIER:
                        break

                terminator_seq = s[terminator_start: terminator_end]
                terminator_end += 1

                while terminator_end < len(s):
                    if s[terminator_end: terminator_end + len(terminator_seq)] == terminator_seq:
                        terminator_end += len(terminator_seq)
                        break
                    else:
                        verified_s += s[terminator_end] # as is
                        terminator_end += 1

                index = terminator_end - 1

            escape_mode = False
            index += 1
        
        else:

            if s[index] == '\\':
                escape_mode = True
                index += 1
                continue

            if not is_valid_codepoint(s[index]):
                raise UnicodeDecodeError('utf-8', s, index, index, 'Disallowed Unicode codepoint category')

            verified_s += s[index]
            index += 1

    return verified_s