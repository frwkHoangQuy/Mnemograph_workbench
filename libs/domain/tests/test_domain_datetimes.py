from datetime import UTC, datetime, timedelta, timezone

import pytest
from mnemograph_domain import ensure_aware_utc


def test_aware_utc_datetime_round_trips_unchanged() -> None:
    value = datetime(2026, 7, 20, 8, 0, tzinfo=UTC)
    assert ensure_aware_utc(value) is value


def test_non_utc_aware_datetime_is_normalized_to_utc() -> None:
    value = datetime(2026, 7, 20, 15, 0, tzinfo=timezone(timedelta(hours=7)))
    assert ensure_aware_utc(value) == datetime(2026, 7, 20, 8, 0, tzinfo=UTC)


def test_naive_datetime_is_rejected() -> None:
    with pytest.raises(ValueError, match="timezone-aware"):
        ensure_aware_utc(datetime(2026, 7, 20, 8, 0))
