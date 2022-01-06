from __future__ import annotations

from uuid import UUID
from typing import Union
from decimal import Decimal
from ce.primitive_types import BinaryFloat
from collections.abc import Mapping, Sequence
from ce.complex_types import Rid, Time, Timestamp

class Map(Mapping):

    """
    A container that implements erroring on duplicate entries,
    and validates each key is of Keyable type only.
    """

    def __init__(self, items: list[KeyValue]):

        self.map = {}
        for (k, v) in items:
            key, value = self.__validated_key_pair(k, v)
            self.map[key] = value

    def __validated_key_pair(self, key, value):

        if not isinstance(key, Keyable):
            raise Exception(f"Key {key} of type {type(key)} is not keyable")

        if not isinstance(value, Value):
            raise Exception(f"Cannot store value {value}, type {type(value)} not in {Value}")

        if key in self.map:
            raise Exception(f"Key {key} already exists")

        return (key, value)

    def __getitem__(self, key):
        return self.map.__getitem__(key)

    def __iter__(self):
        return self.map.__iter__()

    def __len__(self):
        return self.map.__len__()

    def __repr__(self):
        return self.map.__repr__()

Value = Union[str, int, bool, None, Rid, Time, Timestamp, list, Map, Decimal, BinaryFloat]
Keyable = str | Decimal | BinaryFloat | int | Rid | Time | Timestamp | UUID
KeyValue = tuple[Keyable, Value]