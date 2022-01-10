import leb128
from math import ceil
from ce.primitive_types import BinaryFloat
from ce.complex_types import Time, Timestamp, Rid
from ce.container_types import Map, Value


def dump(structure: Value):

    document = b"\x83\x01"

    if isinstance(structure, bool):
        document += b"\x7d" if structure else b"\x7c"
    elif isinstance(structure, int):
        byte_length = lambda x: ceil(x.bit_length() // 8)

        if 100 < abs(structure) < (1 << 8):
            pass
        elif (1 << 8) < abs(structure) < (1 << 16):
            document += b"\x6a" if structure > 0 else b"\x6b"
        elif (1 << 16) < abs(structure) < (1 << 32):
            document += b"\x6c" if structure > 0 else b"\x6d"
        elif (1 << 32) < abs(structure) < (1 << 64):
            document += b"\x6e" if structure > 0 else b"\x6f"
        else:
            document += b"\x66" if structure > 0 else b"\x67"
            document += leb128.u.encode(byte_length(structure))

        document += structure.to_bytes(byte_length, "little", signed=True)

    else:
        


def load(s: bytes):
    pass
