"""Canonical NBA entity schemas.

Entities:
    Team, Player, Game, TeamGame, PlayerGame, TeamSeason, PlayerSeason.

Shared, stable identifiers let historical entities be joined consistently
across seasons even when rosters, names, or cities change.
"""

from __future__ import annotations

from datetime import date
from typing import Literal

import pydantic

from .temporal import TemporalRecord


class Team(pydantic.BaseModel):
    """An NBA franchise, independent of any particular season.

    ``team_id`` is the canonical stable identifier. Franchise relocations or
    renames are represented as separate teams with historical
    :class:`TeamSeason` associations.
    """

    model_config = pydantic.ConfigDict(frozen=True)

    team_id: str
    name: str
    abbreviation: str
    city: str
    conference: str | None = None
    division: str | None = None


class Player(pydantic.BaseModel):
    """An NBA player, independent of any particular team or season."""

    model_config = pydantic.ConfigDict(frozen=True)

    player_id: str
    full_name: str
    first_name: str
    last_name: str
    position: str | None = None
    height_inches: int | None = None
    weight_pounds: int | None = None
    birth_date: date | None = None
    country: str | None = None


class Game(TemporalRecord):
    """A scheduled or completed NBA game."""

    game_id: str
    season: int
    season_type: Literal["regular", "playoffs"]
    home_team_id: str
    away_team_id: str
    home_score: int | None = None
    away_score: int | None = None
    status: Literal[
        "scheduled", "in_progress", "completed", "postponed", "cancelled"
    ] = "scheduled"
    venue: str | None = None

    @pydantic.field_validator("season", mode="after")
    @classmethod
    def _season_positive(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("season must be positive")
        return value


class TeamGame(TemporalRecord):
    """A single team's performance in one game."""

    game_id: str
    team_id: str
    opponent_team_id: str
    is_home: bool
    score: int
    opponent_score: int
    field_goals_made: int | None = None
    field_goals_attempted: int | None = None
    three_pointers_made: int | None = None
    three_pointers_attempted: int | None = None
    free_throws_made: int | None = None
    free_throws_attempted: int | None = None
    rebounds: int | None = None
    assists: int | None = None
    steals: int | None = None
    blocks: int | None = None
    turnovers: int | None = None
    personal_fouls: int | None = None

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def win(self) -> bool:
        """Whether this team won the game."""
        return self.score > self.opponent_score

    @pydantic.field_validator("score", "opponent_score", mode="after")
    @classmethod
    def _score_non_negative(cls, value: int) -> int:
        if value < 0:
            raise ValueError("score cannot be negative")
        return value


class PlayerGame(TemporalRecord):
    """A single player's statistical line for one game."""

    game_id: str
    player_id: str
    team_id: str
    minutes: float | None = None
    points: int | None = None
    rebounds: int | None = None
    assists: int | None = None
    steals: int | None = None
    blocks: int | None = None
    turnovers: int | None = None
    personal_fouls: int | None = None
    field_goals_made: int | None = None
    field_goals_attempted: int | None = None
    three_pointers_made: int | None = None
    three_pointers_attempted: int | None = None
    free_throws_made: int | None = None
    free_throws_attempted: int | None = None
    starter: bool | None = None
    plus_minus: float | None = None

    @pydantic.field_validator("minutes", mode="after")
    @classmethod
    def _minutes_non_negative(cls, value: float | None) -> float | None:
        if value is not None and value < 0:
            raise ValueError("minutes cannot be negative")
        return value


class TeamSeason(pydantic.BaseModel):
    """Historical team membership within a single season.

    Preserves the team's name, abbreviation, city, conference, and division
    as they were in that season, so historical records stay accurate even
    after a franchise relocates or renames.
    """

    model_config = pydantic.ConfigDict(frozen=True)

    team_id: str
    season: int
    name: str
    abbreviation: str
    city: str
    conference: str | None = None
    division: str | None = None

    @pydantic.field_validator("season", mode="after")
    @classmethod
    def _season_positive(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("season must be positive")
        return value


class PlayerSeason(pydantic.BaseModel):
    """Historical player-team association within a single season."""

    model_config = pydantic.ConfigDict(frozen=True)

    player_id: str
    season: int
    team_id: str
    jersey_number: int | None = None
    position: str | None = None

    @pydantic.field_validator("season", mode="after")
    @classmethod
    def _season_positive(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("season must be positive")
        return value
