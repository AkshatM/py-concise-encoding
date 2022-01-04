# Type System

CE documents represent abstract types with the following schema:

```
integers -> ints (native type)
float (except NaN, sNaN) -> floats (native type)
float (NaN, sNaN) -> decimal.Decimal("NaN"), decimal.Decimal("sNaN")
strings -> strings (native type)
null -> None
bool -> bools (native type)
UIDs -> uuid.UUID(s: str)
RIDs -> ce.RID(s: str)
Time -> ce.Time(hours: str|int, minutes: str|int, seconds:, microseconds, timezone)
Timestamp -> ce.Timestamp(year, month, day, ce.Time (optional))
Typed Arrays -> ce.Array(type: ce.Array.TypeEnum, contents: List[str] | List[TypeEnum type])
Lists -> List (native type)
Maps -> ce.Map that maps ints, floats, strings, ce.RIDs, ce.Reference types to one of the above types
more to be added
```