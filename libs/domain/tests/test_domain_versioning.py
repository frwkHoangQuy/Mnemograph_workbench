import pytest
from mnemograph_domain import AggregateVersion, make_aggregate_version


def test_make_aggregate_version_accepts_non_negative_ints() -> None:
    version = make_aggregate_version(0)

    assert version == 0
    assert isinstance(version, int)

    next_version = make_aggregate_version(12)

    assert next_version == 12


def test_make_aggregate_version_rejects_negative_values() -> None:
    with pytest.raises(ValueError, match="non-negative"):
        make_aggregate_version(-1)


def test_make_aggregate_version_rejects_non_integer_values() -> None:
    for invalid_value in (1.5, "2", object()):
        with pytest.raises(ValueError, match="must be an int"):
            make_aggregate_version(invalid_value)  # type: ignore[arg-type]


def test_make_aggregate_version_rejects_bool_values() -> None:
    with pytest.raises(ValueError, match="not bool"):
        make_aggregate_version(True)


def test_aggregate_version_alias_name_is_stable() -> None:
    assert AggregateVersion.__name__ == "AggregateVersion"
