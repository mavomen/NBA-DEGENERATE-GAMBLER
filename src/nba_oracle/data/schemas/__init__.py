"""Canonical NBA entity schemas and dataset metadata."""

from .entities import Game, Player, PlayerGame, PlayerSeason, Team, TeamGame, TeamSeason
from .metadata import DatasetMetadata
from .temporal import TemporalRecord, ensure_utc, utc_now

__all__ = [
    "DatasetMetadata",
    "Game",
    "Player",
    "PlayerGame",
    "PlayerSeason",
    "Team",
    "TeamGame",
    "TeamSeason",
    "TemporalRecord",
    "ensure_utc",
    "utc_now",
]
