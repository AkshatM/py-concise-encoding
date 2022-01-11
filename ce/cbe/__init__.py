import leb128
from math import ceil
from ce.primitive_types import write_int_binary, BinaryFloat
from ce.complex_types import Time, Timestamp, Rid
from ce.container_types import Map, Value


def dump(structure: Value):

    document = b"\x83\x01"

    match structure:
        case bool():
            document += b"\x7d" if structure else b"\x7c"
        case int():
            document += write_int_binary(structure)


def load(s: bytes):
    pass
