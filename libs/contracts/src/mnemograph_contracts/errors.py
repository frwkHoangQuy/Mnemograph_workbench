from typing import Literal

import pydantic
from pydantic import Field

from mnemograph_contracts._base import ContractModel
from mnemograph_contracts.enums import ValidationErrorCode


class ValidationIssue(ContractModel):
    path: tuple[str | int, ...]
    code: ValidationErrorCode


class ValidationErrorEnvelope(ContractModel):
    code: Literal["VALIDATION_ERROR"]
    issues: tuple[ValidationIssue, ...] = Field(min_length=1)


def _map_pydantic_error_type(error_type: str) -> ValidationErrorCode:
    mapping = {
        "missing": ValidationErrorCode.REQUIRED,
        "union_tag_not_found": ValidationErrorCode.REQUIRED,
        "extra_forbidden": ValidationErrorCode.UNKNOWN_FIELD,
        "uuid_parsing": ValidationErrorCode.INVALID_UUID,
        "uuid_type": ValidationErrorCode.INVALID_TYPE,
        "is_instance_of": ValidationErrorCode.INVALID_TYPE,
        "string_type": ValidationErrorCode.INVALID_TYPE,
        "int_type": ValidationErrorCode.INVALID_TYPE,
        "tuple_type": ValidationErrorCode.INVALID_TYPE,
        "model_type": ValidationErrorCode.INVALID_TYPE,
        "enum": ValidationErrorCode.INVALID_ENUM,
        "literal_error": ValidationErrorCode.INVALID_ENUM,
        "union_tag_invalid": ValidationErrorCode.INVALID_ENUM,
        "greater_than_equal": ValidationErrorCode.OUT_OF_RANGE,
        "greater_than": ValidationErrorCode.OUT_OF_RANGE,
        "less_than_equal": ValidationErrorCode.OUT_OF_RANGE,
        "less_than": ValidationErrorCode.OUT_OF_RANGE,
        "string_too_short": ValidationErrorCode.OUT_OF_RANGE,
        "too_short": ValidationErrorCode.OUT_OF_RANGE,
        "datetime_type": ValidationErrorCode.INVALID_TYPE,
        "datetime_parsing": ValidationErrorCode.INVALID_TYPE,
        "datetime_from_date_parsing": ValidationErrorCode.INVALID_TYPE,
        "datetime_object_invalid": ValidationErrorCode.INVALID_TYPE,
        "naive_datetime": ValidationErrorCode.NAIVE_DATETIME,
    }
    return mapping.get(error_type, ValidationErrorCode.INVALID_VALUE)


def _validation_error_to_envelope(
    error: pydantic.ValidationError,
) -> ValidationErrorEnvelope:
    issues = []
    for item in error.errors():
        error_type_obj = item.get("type", "")
        error_type = error_type_obj if isinstance(error_type_obj, str) else str(error_type_obj)
        loc_value = item.get("loc", ())
        location: tuple[object, ...]
        if isinstance(loc_value, tuple):
            location = loc_value
        elif isinstance(loc_value, list):
            location = tuple(loc_value)
        else:
            location = (str(loc_value),)

        normalized_loc: tuple[str | int, ...] = tuple(
            segment if isinstance(segment, (str, int)) else str(segment) for segment in location
        )

        issues.append(
            ValidationIssue(
                path=normalized_loc,
                code=_map_pydantic_error_type(error_type),
            )
        )

    if not issues:
        issues = [ValidationIssue(path=(), code=ValidationErrorCode.INVALID_VALUE)]

    return ValidationErrorEnvelope(
        code="VALIDATION_ERROR",
        issues=tuple(issues),
    )
