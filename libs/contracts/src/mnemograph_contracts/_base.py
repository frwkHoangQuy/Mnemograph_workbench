from collections.abc import Mapping
from datetime import UTC, datetime
from typing import Annotated, cast

from pydantic import AfterValidator, BaseModel, ConfigDict
from pydantic_core import PydanticCustomError


class ContractModel(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid", frozen=True)


def ensure_aware_utc(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise PydanticCustomError("naive_datetime", "naive_datetime")
    return value.astimezone(UTC)


UtcDateTime = Annotated[datetime, AfterValidator(ensure_aware_utc)]


def _extract_string_tag(
    value: object,
    field_name: str,
) -> str | None:
    raw: object
    if isinstance(value, Mapping):
        mapping = cast(Mapping[str, object], value)
        raw = mapping.get(field_name)
    else:
        raw = cast(object, getattr(value, field_name, None))

    if not isinstance(raw, str):
        return None

    return str(raw)
