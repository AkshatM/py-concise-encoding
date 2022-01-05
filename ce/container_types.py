from uuid import UUID
from typing import Union
from collections.abc import Mapping, Sequence
from ce.complex_types import Rid, Time, Timestamp

Value = Union[str, float, int, bool, None, Rid, Time, Timestamp, "Map", UUID, "List"]
Keyable = str | float | int | Rid | Time | Timestamp | UUID
KeyValue = tuple[Keyable, Value]


class List(Sequence):
    def __init__(self, items: list[Value]):
        self.list = [item for item in items]

    def __getitem__(self, index):
        return self.list[index]

    def __len__(self):
        return len(self.list)

    def __eq__(self, other):
        if isinstance(other, List):
            if len(self.list) == len(other.list):
                return all(self.list[i] == other.list[i] for i in range(len(self.list)))

    def __repr__(self):
        return f"List{self.list}"


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

        import pdb; pdb.set_trace()
        if not isinstance(value, Value):
            raise Exception(f"Cannot store value {value} of type {type(value)}")

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
