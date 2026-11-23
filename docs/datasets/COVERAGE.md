# NBA Dataset Coverage Matrix

**Version:** 0.1.0  
**Status:** Draft  
**Owner:** Data Source Research (E01)  
**Related:** `PRD.md` §8, `FEATURE-LIST.md` E01/E02, `AGENTS.md` §4.6

---

## Purpose

This document records every candidate NBA data source investigated for the project, its historical coverage, timestamp granularity, licensing terms, known limitations, and priority tier. It exists so ingestion adapters (E02) can be built against a defensible source decision rather than an assumption that an endpoint is reliable merely because it once responded.

All sources are treated as **replaceable adapters**. Internal canonical schemas (`nba_oracle.data.schemas`) never depend on one provider's response format (ARCHITECTURE.md §3.1, §3.2).

## Priority Definitions

| Priority | Meaning |
|---|---|
| P0 | Required for initial usable release: game results, box scores, team/player statistics, schedules and game metadata. |
| P1 | Required for complete platform: injuries and player availability, timestamped sportsbook odds. |
| P2 | Advanced research: player prop odds, advanced tracking statistics. |

## Coverage Matrix

| Source | Type | Coverage Window | Update Frequency | Timestamp Granularity | License | Priority | Known Limitations |
|---|---|---|---|---|---|---|---|
| `nba_api` (stats.nba.com) | Official stats API (unofficial client) | Historical through current season; exact earliest season endpoint-dependent | Live / on request | `event_time` (game date), `available_at` not guaranteed by endpoint | Not documented (NBA.com Terms of Use apply) | P0 | NBA.com does not publish changelogs; endpoints can be renamed or retired without notice; static player/team reference data is only as fresh as the package release; no `available_at` provenance; rate limits and timeouts required; results may be revised after posting |
| hamzas/nba-games (Hugging Face) | Public historical dataset (CSV → Parquet) | Games through 2025-02-13 | Updated daily (per dataset card) | Game date only; `available_at` not provided | Unknown | P0 | Small effective sample for deep history relative to full NBA history; license unstated; completeness gaps possible; no odds or injury timestamps |
| eoinamoore/historical-nba-data-and-player-box-scores (Kaggle) | Public historical dataset | Every NBA game since 1947; advanced stats since 1996 | Updated daily (per dataset card) | Game date only; `available_at` not provided | CC0 Public Domain | P0 | Described as "updated nightly" with known upload interruptions; completeness gaps possible; no odds or injury timestamps; redistribution licensing CC0 |
| NocturneBear/NBA-Data-2010-2024 (GitHub) | Public historical dataset (CSV) | 2010–2024 regular season + playoffs | Static snapshot (no updates) | Game date only; `available_at` not provided | MIT License | P0 | Fixed 15-year window; not maintained; no `available_at`; no odds or injury timestamps |
| wyattowalsh/nba-db (Kaggle/GitHub) | Public historical database (SQLite) | Every game since inaugural 1946-47 season; box scores for ~95% of games; play-by-play 13M+ rows | Daily updater notebooks available | Game date only; `available_at` not provided | Not documented | P0 | Box-score coverage incomplete (~95%); play-by-play starts 1996; no `available_at`; no odds or injury timestamps |

### Sources intentionally deferred (not P0)

| Source | Type | Priority | Reason |
|---|---|---|---|
| Injury reports (NBA.com official) | Official | P1 | Coverage and historical timestamp availability not yet verified; player availability is P1 per PRD §8.1. |
| Sportsbook odds (timestamped) | Market provider | P1 | No source identified with guaranteed timestamped snapshots at decision time; closing odds must not be treated as historically available (AGENTS §4.3). |
| Player prop odds | Market provider | P2 | Prop market coverage and timestamp granularity unverified; P2 per PRD §8.1. |
| Play-by-play / advanced tracking | Public datasets | P1/P2 | Available in some sources above but not required for initial baselines. |

## Timestamp Fields

Per AGENTS §4.2 and PRD §6.2, every time-sensitive record distinguishes:

| Field | Meaning |
|---|---|
| `event_time` | When the real-world event (game) occurred. |
| `available_at` | When the information became available to a forecaster. |
| `prediction_timestamp` | When a forecast was generated. |

None of the candidate sources above document `available_at` reliably. Game dates provide `event_time`; `available_at` must be treated as unknown or conservatively approximated (e.g., game date + box-score publication lag) until a source documents publication timestamps. **`available_at` must never be conflated with `event_time`** — doing so introduces look-ahead bias into historical forecasts (AGENTS §4.3).

## Look-Ahead Bias Constraints

- Historical closing odds are **not** prices available at earlier decision times. Market simulation (E12) requires timestamped odds snapshots corresponding to the simulated decision time (PRD §6.11, AGENTS §5.6).
- Final game statistics must not enter features used to predict that same game (AGENTS §4.3).
- Post-game statistics and corrections must not leak into pre-game predictions.
- Rolling features must exclude the target game.

## Licensing and Redistribution

- No raw data, large historical datasets, or downloaded snapshots are committed to Git (AGENTS §9.1).
- `uv.lock` and `pyproject.toml` track only code dependencies; no paid or mandatory data providers are added (PRD §7.1, AGENTS §9.3).
- License terms recorded here are best-effort summaries from public dataset cards; each adapter must validate the actual source license before use (AGENTS §4.6).
- Sources without a documented license (nba_api NBA.com Terms of Use, hamzas/nba-games, wyattowalsh/nba-db) require explicit review before ingestion.

## Data Gaps and Biases

| Gap / Bias | Consequence | Mitigation |
|---|---|---|
| `available_at` not documented by candidate sources | Cannot reconstruct exactly what was known at prediction time | Document conservatively; treat missing availability as unknown, not fabricated |
| Injury and availability history incomplete | Player-level predictions may use future availability | Mark P1; do not infer availability that cannot be verified historically |
| Box-score coverage incomplete (~95% in nba-db) | Missing games reduce evaluation sample | Report missingness explicitly; never silently impute |
| Endpoint churn (nba_api) | Adapter may break without notice | Replaceable adapter design; pin versions; monitor endpoint stability |
| Static reference data staleness | Team/player IDs may lag roster changes | Use historical identity resolution (`TeamSeason`, `PlayerSeason`) |

## Recommendation for E02

Start ingestion with a P0 source that documents game results, box scores, and team/player statistics with stable identifiers, then layer E04 validation on top. The `nba_api` client is the most comprehensive live endpoint surface but requires tolerance for endpoint churn; public static datasets (eoinamoore CC0, NocturneBear MIT) provide verifiable historical coverage for baseline development but are not maintained. Final source selection and adapter implementation belong to E02 and must be recorded in an ADR (docs/decisions/).

## Open Questions

- Which source provides the earliest verifiable `available_at` timestamp for game results and box scores?
- Is any timestamped odds source available with snapshot granularity sufficient for P1 market research?
- What is the actual redistribution license for nba_api-driven NBA.com data and wyattowalsh/nba-db?
