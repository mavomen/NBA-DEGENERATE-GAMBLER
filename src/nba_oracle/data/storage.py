"""Persistent storage for canonical datasets.

Parquet files live under ``<root>/<entity>/season=YYYY/<entity>.parquet``
(F03-08). DuckDB executes analytical queries directly over those Parquet
files without loading entire datasets into memory (F03-09).
"""

from __future__ import annotations

import os
from collections.abc import Sequence
from pathlib import Path

import duckdb
import polars as pl

DEFAULT_ROOT = Path(
    os.environ.get(
        "NBA_ORACLE_DATA_ROOT",
        Path(__file__).resolve().parents[3] / "data" / "processed",
    )
)


def _validate_entity(entity: str) -> str:
    """Reject entity names that could escape the storage root via path traversal."""
    parts = Path(entity).parts
    if (
        not entity
        or Path(entity).is_absolute()
        or Path(entity).name != entity
        or any(part in {"..", ""} for part in parts)
    ):
        raise ValueError(f"invalid entity name: {entity!r}")
    return entity


def _entity_dir(root: str | Path, entity: str) -> Path:
    _validate_entity(entity)
    return Path(root) / entity


def _season_dir(root: str | Path, entity: str, season: int) -> Path:
    return _entity_dir(root, entity) / f"season={season}"


def _parquet_path(root: str | Path, entity: str, season: int) -> Path:
    return _season_dir(root, entity, season) / f"{entity}.parquet"


def write_dataset(
    df: pl.DataFrame,
    entity: str,
    season: int,
    root: str | Path = DEFAULT_ROOT,
    sort_columns: Sequence[str] | None = None,
) -> Path:
    """Write a DataFrame to a deterministic Parquet partition.

    Layout: ``<root>/<entity>/season=YYYY/<entity>.parquet``. When
    ``sort_columns`` is given, rows are sorted by those columns so equivalent
    inputs produce deterministic output; otherwise the input row order is
    preserved. Existing partition files are overwritten.
    """
    root_path = Path(root)
    season_dir = _season_dir(root_path, entity, season)
    season_dir.mkdir(parents=True, exist_ok=True)
    target = _parquet_path(root_path, entity, season)
    if sort_columns is not None:
        ordered = df.sort(list(sort_columns))
    else:
        ordered = df
    ordered.write_parquet(target)
    return target


def read_dataset(
    entity: str, season: int, root: str | Path = DEFAULT_ROOT
) -> pl.DataFrame:
    """Read one season partition for an entity."""
    target = _parquet_path(Path(root), entity, season)
    return pl.read_parquet(target)


def read_entity(entity: str, root: str | Path = DEFAULT_ROOT) -> pl.LazyFrame:
    """Lazily scan every season partition for an entity (bounded memory).

    Partition columns (season) are recovered from the directory names. Call
    :meth:`polars.LazyFrame.collect` only after filtering or slicing.
    """
    _validate_entity(entity)
    entity_path = Path(root) / entity
    if not entity_path.is_dir():
        return pl.DataFrame().lazy()
    return scan_entity(entity, root)


def list_seasons(entity: str, root: str | Path = DEFAULT_ROOT) -> list[int]:
    """Return the seasons persisted for an entity, in ascending order."""
    entity_path = _entity_dir(root, entity)
    if not entity_path.is_dir():
        return []
    seasons: list[int] = []
    for child in entity_path.iterdir():
        if child.is_dir() and child.name.startswith("season="):
            seasons.append(int(child.name.split("=", 1)[1]))
    return sorted(seasons)


def scan_entity(entity: str, root: str | Path = DEFAULT_ROOT) -> pl.LazyFrame:
    """Lazily scan all partitions for an entity (bounded memory)."""
    pattern = str(_entity_dir(root, entity) / "season=*" / f"{entity}.parquet")
    return pl.scan_parquet(pattern, hive_partitioning=True)


def parquet_glob(entity: str, root: str | Path = DEFAULT_ROOT) -> str:
    """Glob pattern matching all Parquet files for an entity, for DuckDB."""
    return str(_entity_dir(root, entity) / "season=*" / f"{entity}.parquet")


def duckdb_query(sql: str, parameters: Sequence | None = None) -> pl.DataFrame:
    """Execute a DuckDB SQL query directly over Parquet files.

    DuckDB reads Parquet files on demand, but the full result set is
    materialized into memory (pyarrow is not a dependency, so the zero-copy
    ``.pl()`` path is unavailable). For large scans, add ``LIMIT`` or
    partition filters to the SQL. Results are returned as a Polars DataFrame.
    """
    relation = duckdb.sql(sql, params=list(parameters or []))
    rows = relation.fetchall()
    columns = [desc[0] for desc in relation.description] if relation.description else []
    return pl.DataFrame(rows, schema=columns) if columns else pl.DataFrame()
