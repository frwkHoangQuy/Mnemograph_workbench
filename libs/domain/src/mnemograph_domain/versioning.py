from typing import NewType

AggregateVersion = NewType("AggregateVersion", int)


def make_aggregate_version(value: int) -> AggregateVersion:
    if isinstance(value, bool):
        raise ValueError("AggregateVersion must be an int, not bool")
    if not isinstance(value, int):
        raise ValueError("AggregateVersion must be an int")
    if value < 0:
        raise ValueError("AggregateVersion must be non-negative")
    return AggregateVersion(value)
