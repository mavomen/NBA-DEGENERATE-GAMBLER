"""Unit tests for Parquet and DuckDB storage."""

from __future__ import annotations

from datetime import UTC, datetime

import polars as pl
import pytest

from nba_oracle.data.storage import (
    DEFAULT_ROOT,
    duckdb_query,
    list_seasons,
    parquet_glob,
    read_dataset,
    read_entity,
    scan_entity,
    write_dataset,
)

NOW = datetime(2024, 11, 1, 19, 30, tzinfo=UTC)


def _game_frame() -> pl.DataFrame:
    return pl.DataFrame(
        {
            "game_id": ["G1", "G2"],
            "home_team_id": ["LAL", "LAL"],
            "away_team_id": ["GSW", "BOS"],
            "event_time": [NOW, NOW],
            "available_at": [NOW, NOW],
            "home_score": [110, 102],
            "away_score": [105, 99],
        }
    )


def test_write_and_read_roundtrip(tmp_path) -> None:
    df = _game_frame()
    path = write_dataset(df, "games", 2024, root=tmp_path)

    assert path == tmp_path / "games" / "season=2024" / "games.parquet"
    assert path.is_file()

    result = read_dataset("games", 2024, root=tmp_path)
    assert result.sort("game_id").equals(df.sort("game_id"))


def test_write_is_deterministic(tmp_path) -> None:
    df = _game_frame()
    first = write_dataset(df, "games", 2024, root=tmp_path)
    second = write_dataset(df, "games", 2024, root=tmp_path)

    assert first == second
    assert first.read_bytes() == second.read_bytes()


def test_read_entity_combines_seasons(tmp_path) -> None:
    first = pl.DataFrame(
        {
            "game_id": ["G1"],
            "home_team_id": ["LAL"],
            "away_team_id": ["GSW"],
            "event_time": [NOW],
            "available_at": [NOW],
            "home_score": [110],
            "away_score": [105],
        }
    )
    second = pl.DataFrame(
        {
            "game_id": ["G2"],
            "home_team_id": ["LAL"],
            "away_team_id": ["BOS"],
            "event_time": [NOW],
            "available_at": [NOW],
            "home_score": [102],
            "away_score": [99],
        }
    )
    write_dataset(first, "games", 2024, root=tmp_path)
    write_dataset(second, "games", 2025, root=tmp_path)

    combined = read_entity("games", root=tmp_path).collect()
    assert combined.height == 2
    assert set(combined["season"].to_list()) == {2024, 2025}
    assert list_seasons("games", root=tmp_path) == [2024, 2025]


def test_read_dataset_missing_partition_raises(tmp_path) -> None:
    with pytest.raises(FileNotFoundError):
        read_dataset("games", 2024, root=tmp_path)


def test_read_entity_unknown_entity_returns_empty(tmp_path) -> None:
    assert read_entity("nope", root=tmp_path).collect().is_empty()
    assert list_seasons("nope", root=tmp_path) == []


def test_scan_entity_is_lazy_and_complete(tmp_path) -> None:
    df = _game_frame()
    write_dataset(df, "games", 2024, root=tmp_path)

    lazy = scan_entity("games", root=tmp_path)
    assert isinstance(lazy, pl.LazyFrame)
    assert lazy.collect().height == 2


def test_duckdb_query_over_parquet(tmp_path) -> None:
    df = _game_frame()
    write_dataset(df, "games", 2024, root=tmp_path)
    write_dataset(
        df.with_row_index("offset").with_columns(game_id=pl.col("game_id") + "_b"),
        "games",
        2025,
        root=tmp_path,
    )

    pattern = parquet_glob("games", root=tmp_path)
    result = duckdb_query(
        "SELECT count(*) AS n FROM read_parquet(?, hive_partitioning=1)",
        [pattern],
    )
    assert result["n"][0] == 4


def test_duckdb_query_filters_by_partition(tmp_path) -> None:
    write_dataset(_game_frame(), "games", 2024, root=tmp_path)

    pattern = parquet_glob("games", root=tmp_path)
    result = duckdb_query(
        "SELECT count(*) AS n FROM read_parquet(?, hive_partitioning=1) WHERE season = ?",
        [pattern, 2024],
    )
    assert result["n"][0] == 2


def test_write_empty_dataframe(tmp_path) -> None:
    empty = pl.DataFrame(
        {
            "game_id": [],
            "home_team_id": [],
            "away_team_id": [],
            "event_time": [],
            "available_at": [],
            "home_score": [],
            "away_score": [],
        }
    )
    path = write_dataset(empty, "games", 2024, root=tmp_path)
    assert path.is_file()
    assert read_dataset("games", 2024, root=tmp_path).is_empty()


def test_default_root_constant() -> None:
    assert DEFAULT_ROOT.is_absolute()
    assert str(DEFAULT_ROOT).endswith("data/processed")


def test_write_dataset_rejects_traversing_entity(tmp_path) -> None:
    df = pl.DataFrame({"game_id": ["G1"]})
    with pytest.raises(ValueError, match="invalid entity name"):
        write_dataset(df, "../../evil", 2024, root=tmp_path)


def test_read_dataset_rejects_traversing_entity(tmp_path) -> None:
    with pytest.raises(ValueError, match="invalid entity name"):
        read_dataset("../evil", 2024, root=tmp_path)


def test_entity_name_with_slash_rejected() -> None:
    from nba_oracle.data.storage import _validate_entity

    with pytest.raises(ValueError):
        _validate_entity("a/b")


def test_entity_name_with_dotdot_rejected() -> None:
    from nba_oracle.data.storage import _validate_entity

    with pytest.raises(ValueError):
        _validate_entity("..")
