import pytest
from mnemograph_domain import AggregateVersion, make_aggregate_version


def test_make_aggregate_version_accepts_non_negative_ints() -> None:
    assert make_aggregate_version(0) == 0
    assert make_aggregate_version(7) == 7


def test_make_aggregate_version_rejects_negative_values() -> None:
    with pytest.raises(ValueError):
        make_aggregate_version(-1)


def test_make_aggregate_version_rejects_non_integer_values() -> None:
    for invalid_value in (1.5, "2", object(), None):
        with pytest.raises(ValueError):
            make_aggregate_version(invalid_value)  # type: ignore[arg-type]


def test_make_aggregate_version_rejects_true_and_false() -> None:
    with pytest.raises(ValueError):
        make_aggregate_version(True)
    with pytest.raises(ValueError):
        make_aggregate_version(False)


def test_aggregate_version_alias_name_is_stable() -> None:
    assert AggregateVersion.__name__ == "AggregateVersion"


def test_aggregate_version_direct_constructor_is_identity_and_non_validating() -> None:
    assert AggregateVersion(-3) == -3
    assert AggregateVersion(True) == 1


def test_make_aggregate_version_is_the_validating_boundary() -> None:
    assert make_aggregate_version(3) == AggregateVersion(3)
    with pytest.raises(ValueError):
        make_aggregate_version(-3)
