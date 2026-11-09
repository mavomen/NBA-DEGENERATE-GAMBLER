"""Canonical temporal fields and helpers.

The system distinguishes three timestamps (PRD.md section 6.2,
ARCHITECTURE.md section 4.3):

- ``event_time``: when the real-world event occurred.
- ``available_at``: when the information became available.
- ``prediction_timestamp``: when a forecast was generated.

These must never be treated as interchangeable; doing so introduces
look-ahead bias into historical forecasts.
"""

from __future__ import annotations

from datetime import UTC, datetime

import pydantic


def utc_now() -> datetime:
    """Return the current moment as an aware UTC datetime."""
    return datetime.now(UTC)


def ensure_utc(value: datetime) -> datetime:
    """Return ``value`` as an aware UTC datetime.

    Naive datetimes are rejected explicitly. Silently assuming a timezone is a
    source of temporal bugs.
    """
    if value.tzinfo is None:
        raise ValueError("datetime must be timezone-aware")
    return value.astimezone(UTC)


class TemporalRecord(pydantic.BaseModel):
    """Base model for records carrying ``event_time`` and ``available_at``."""

    event_time: datetime
    available_at: datetime

    @pydantic.field_validator("event_time", "available_at", mode="after")
    @classmethod
    def _require_aware_utc(cls, value: datetime) -> datetime:
        return ensure_utc(value)
