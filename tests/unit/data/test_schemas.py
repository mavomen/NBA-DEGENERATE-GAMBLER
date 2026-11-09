"""Unit tests for canonical entity and metadata schemas."""

from __future__ import annotations

from datetime import UTC, date, datetime

import pytest
from pydantic import ValidationError

from nba_oracle.data.schemas import (
    DatasetMetadata,
    Game,
    Player,
    PlayerGame,
    PlayerSeason,
    Team,
    TeamGame,
    TeamSeason,
    TemporalRecord,
    utc_now,
)

NOW = datetime(2024, 11, 1, 19, 30, tzinfo=UTC)


def test_team_valid() -> None:
    team = Team(
        team_id="LAL",
        name="Los Angeles Lakers",
        abbreviation="LAL",
        city="Los Angeles",
        conference="West",
        division="Pacific",
    )
    assert team.team_id == "LAL"
    assert team.conference == "West"


def test_team_optional_fields_default_to_none() -> None:
    team = Team(
        team_id="LAL", name="Los Angeles Lakers", abbreviation="LAL", city="Los Angeles"
    )
    assert team.conference is None
    assert team.division is None


def test_team_is_frozen() -> None:
    team = Team(
        team_id="LAL", name="Los Angeles Lakers", abbreviation="LAL", city="Los Angeles"
    )
    with pytest.raises(ValidationError):
        team.name = "Renamed"


def test_team_rejects_missing_required() -> None:
    with pytest.raises(ValidationError):
        Team(name="Los Angeles Lakers")


def test_player_valid() -> None:
    player = Player(
        player_id="P1",
        full_name="LeBron James",
        first_name="LeBron",
        last_name="James",
        position="F",
        height_inches=80,
        weight_pounds=250,
        birth_date=date(1984, 12, 30),
        country="USA",
    )
    assert player.player_id == "P1"
    assert player.birth_date == date(1984, 12, 30)


def test_player_is_frozen() -> None:
    player = Player(
        player_id="P1", full_name="LeBron James", first_name="LeBron", last_name="James"
    )
    with pytest.raises(ValidationError):
        player.full_name = "Someone Else"


def test_temporal_record_requires_aware_datetimes() -> None:
    with pytest.raises(ValidationError):
        TemporalRecord(event_time=datetime.now(), available_at=NOW)


def test_temporal_record_converts_to_utc() -> None:
    eastern = datetime(2024, 11, 1, 14, 30, tzinfo=UTC)
    record = TemporalRecord(event_time=eastern, available_at=eastern)
    assert record.event_time.tzinfo is not None


def test_game_valid_completed() -> None:
    game = Game(
        game_id="0022300101",
        season=2024,
        season_type="regular",
        event_time=NOW,
        available_at=NOW,
        home_team_id="LAL",
        away_team_id="GSW",
        home_score=110,
        away_score=105,
        status="completed",
    )
    assert game.game_id == "0022300101"
    assert game.status == "completed"


def test_game_defaults_to_scheduled_without_scores() -> None:
    game = Game(
        game_id="0022300102",
        season=2024,
        season_type="regular",
        event_time=NOW,
        available_at=NOW,
        home_team_id="LAL",
        away_team_id="GSW",
    )
    assert game.status == "scheduled"
    assert game.home_score is None


def test_game_rejects_invalid_status() -> None:
    with pytest.raises(ValidationError):
        Game(
            game_id="G",
            season=2024,
            season_type="regular",
            event_time=NOW,
            available_at=NOW,
            home_team_id="LAL",
            away_team_id="GSW",
            status="final",
        )


def test_game_rejects_non_positive_season() -> None:
    with pytest.raises(ValidationError):
        Game(
            game_id="G",
            season=0,
            season_type="regular",
            event_time=NOW,
            available_at=NOW,
            home_team_id="LAL",
            away_team_id="GSW",
        )


def test_team_game_win_computed() -> None:
    winner = TeamGame(
        game_id="G",
        team_id="LAL",
        opponent_team_id="GSW",
        is_home=True,
        event_time=NOW,
        available_at=NOW,
        score=110,
        opponent_score=105,
    )
    assert winner.win is True

    loser = TeamGame(
        game_id="G",
        team_id="GSW",
        opponent_team_id="LAL",
        is_home=False,
        event_time=NOW,
        available_at=NOW,
        score=105,
        opponent_score=110,
    )
    assert loser.win is False


def test_team_game_rejects_negative_score() -> None:
    with pytest.raises(ValidationError):
        TeamGame(
            game_id="G",
            team_id="LAL",
            opponent_team_id="GSW",
            is_home=True,
            event_time=NOW,
            available_at=NOW,
            score=-1,
            opponent_score=105,
        )


def test_player_game_valid() -> None:
    line = PlayerGame(
        game_id="G",
        player_id="P1",
        team_id="LAL",
        minutes=36.5,
        points=28,
        rebounds=8,
        assists=7,
        starter=True,
        plus_minus=12.5,
        event_time=NOW,
        available_at=NOW,
    )
    assert line.minutes == 36.5
    assert line.points == 28


def test_player_game_rejects_negative_minutes() -> None:
    with pytest.raises(ValidationError):
        PlayerGame(
            game_id="G",
            player_id="P1",
            team_id="LAL",
            minutes=-5.0,
            event_time=NOW,
            available_at=NOW,
        )


def test_team_season_preserves_historical_identity() -> None:
    season = TeamSeason(
        team_id="LAL",
        season=2024,
        name="Los Angeles Lakers",
        abbreviation="LAL",
        city="Los Angeles",
        conference="West",
        division="Pacific",
    )
    assert season.team_id == "LAL"
    assert season.season == 2024
    assert season.name == "Los Angeles Lakers"


def test_team_season_is_frozen() -> None:
    season = TeamSeason(
        team_id="LAL",
        season=2024,
        name="Los Angeles Lakers",
        abbreviation="LAL",
        city="Los Angeles",
    )
    with pytest.raises(ValidationError):
        season.city = "Seattle"


def test_team_season_rejects_non_positive_season() -> None:
    with pytest.raises(ValidationError):
        TeamSeason(
            team_id="LAL",
            season=0,
            name="Lakers",
            abbreviation="LAL",
            city="Los Angeles",
        )


def test_player_season_association() -> None:
    association = PlayerSeason(
        player_id="P1",
        season=2024,
        team_id="LAL",
        jersey_number=23,
        position="F",
    )
    assert association.player_id == "P1"
    assert association.team_id == "LAL"
    assert association.season == 2024


def test_player_season_is_frozen() -> None:
    association = PlayerSeason(player_id="P1", season=2024, team_id="LAL")
    with pytest.raises(ValidationError):
        association.team_id = "GSW"


def test_dataset_metadata_defaults() -> None:
    metadata = DatasetMetadata(
        dataset_id="games-2024",
        version="1.0.0",
        source="nba_stats",
        retrieved_at=NOW,
        available_at=NOW,
    )
    assert metadata.schema_version == "1.0"
    assert metadata.transformation_version == "1.0"
    assert metadata.file_references == []
    assert metadata.record_count is None
    assert metadata.created_at.tzinfo is not None


def test_dataset_metadata_records_file_references() -> None:
    metadata = DatasetMetadata(
        dataset_id="games-2024",
        version="1.0.0",
        source="nba_stats",
        retrieved_at=NOW,
        available_at=NOW,
        file_references=[
            "data/processed/games/season=2024/games.parquet",
        ],
        record_count=1230,
    )
    assert metadata.file_references == [
        "data/processed/games/season=2024/games.parquet"
    ]
    assert metadata.record_count == 1230


def test_dataset_metadata_rejects_naive_timestamps() -> None:
    with pytest.raises(ValidationError):
        DatasetMetadata(
            dataset_id="games-2024",
            version="1.0.0",
            source="nba_stats",
            retrieved_at=datetime.now(),
            available_at=NOW,
        )


def test_utc_now_is_aware() -> None:
    assert utc_now().tzinfo is not None
