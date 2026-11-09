"""Dataset metadata and versioning schema.

Identifies the source, retrieval time, schema version, and transformation
version behind a processed dataset version (F03-06, F03-10).
"""

from __future__ import annotations

from datetime import datetime

import pydantic

from .temporal import ensure_utc, utc_now


class DatasetMetadata(pydantic.BaseModel):
    """Identifying and provenance metadata for a processed dataset version."""

    dataset_id: str
    version: str
    source: str
    source_version: str | None = None
    schema_version: str = "1.0"
    transformation_version: str = "1.0"
    retrieved_at: datetime
    available_at: datetime
    description: str | None = None
    record_count: int | None = None
    file_references: list[str] = pydantic.Field(default_factory=list)
    created_at: datetime = pydantic.Field(default_factory=utc_now)

    @pydantic.field_validator("retrieved_at", "available_at", mode="after")
    @classmethod
    def _require_aware_utc(cls, value: datetime) -> datetime:
        return ensure_utc(value)

    @pydantic.field_validator("file_references", mode="before")
    @classmethod
    def _ensure_list(cls, value: list[str] | None) -> list[str]:
        if value is None:
            return []
        return list(value)
