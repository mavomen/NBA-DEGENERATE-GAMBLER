# TODO

> **Project:** NBA Degenerate Gambler  
> **Principle:** Build the evidence first. Optimize the models second.  
> **Approach:** Research-first, local-first, reproducible, and incremental.

## Status Convention

- `[ ]` Not started
- `[~]` In progress
- `[x]` Completed

Tasks should be marked complete only when their acceptance criteria are satisfied. Remove obsolete tasks rather than keeping an increasingly fictional history of unfinished work.

---

# M0: Project Foundation

Establish a reproducible development environment and define the project's boundaries.

## Repository

- [ ] Define the project's official scope and terminology.
- [ ] Finalize `README.md` with objectives, features, limitations, and setup instructions.
- [ ] Create `AGENTS.md` with project conventions and development instructions.
- [ ] Create `ARCHITECTURE.md`.
- [ ] Create `FEATURE-LIST.md`.
- [ ] Create `.editorconfig`.
- [ ] Create `Makefile` with common development commands.
- [ ] Create `.gitignore` for Python, ML artifacts, datasets, notebooks, and local configuration.
- [ ] Create `pyproject.toml`.
- [ ] Configure Python 3.12+ and `uv`.
- [ ] Configure Ruff for formatting and linting.
- [ ] Configure pytest.
- [ ] Establish the Git branching and commit conventions.
- [ ] Add a GitHub Actions workflow for automated quality checks.
- [ ] Verify that a clean clone can install dependencies and run the checks.

## Development Environment

- [ ] Verify CPU-only execution.
- [ ] Verify optional NVIDIA CUDA support.
- [ ] Establish memory-conscious defaults for local training.
- [ ] Define configuration management using YAML and Pydantic.
- [ ] Separate configuration files from secrets and machine-specific settings.
- [ ] Establish deterministic random seed handling.
- [ ] Define logging and error-reporting conventions.

**Exit criteria:** A clean development environment can be reproduced, configured, and validated without relying on undocumented local state.

---

# M1: Research and Data Discovery

Understand what data exists, what can be collected, and what can legitimately be used in historical simulations.

## Data Source Research

- [ ] Identify reliable sources for historical NBA game results.
- [ ] Identify sources for team-level statistics.
- [ ] Identify sources for player-level statistics.
- [ ] Investigate NBA API endpoint coverage and limitations.
- [ ] Investigate supplementary data sources.
- [ ] Identify sources for player injuries and availability.
- [ ] Investigate historical injury-report availability.
- [ ] Identify sources for schedules, venues, and game metadata.
- [ ] Identify historical betting odds sources.
- [ ] Investigate player prop market data availability.
- [ ] Investigate historical odds snapshot coverage and timestamp granularity.
- [ ] Review data licensing, redistribution, and usage restrictions.

## Dataset Coverage

- [ ] Create `docs/datasets/COVERAGE.md`.
- [ ] Record the earliest and latest available seasons for each source.
- [ ] Record update frequency and collection limitations.
- [ ] Record whether historical publication timestamps are available.
- [ ] Distinguish raw observations from derived statistics.
- [ ] Identify missing seasons, teams, players, and markets.
- [ ] Identify potential data leakage in available datasets.
- [ ] Identify survivorship and selection biases.
- [ ] Define the minimum viable historical dataset.
- [ ] Document known gaps and their consequences.

## Research Decisions

- [ ] Define the initial historical evaluation period.
- [ ] Define supported game markets.
- [ ] Define supported player prop markets.
- [ ] Define the prediction timestamp for each use case.
- [ ] Define which information is considered available at prediction time.
- [ ] Document assumptions that cannot be validated historically.

**Exit criteria:** A documented source and coverage matrix exists. The project can distinguish usable historical information from information that merely happens to exist in a dataset.

---

# M2: Data Ingestion and Storage

Build a reliable, replaceable data collection and storage layer.

## Ingestion

- [ ] Design a common data-source adapter interface.
- [ ] Implement the initial NBA data adapter.
- [ ] Implement historical game-result ingestion.
- [ ] Implement team statistics ingestion.
- [ ] Implement player statistics ingestion.
- [ ] Implement schedule and game metadata ingestion.
- [ ] Implement injury and player availability ingestion where supported.
- [ ] Implement odds ingestion where supported.
- [ ] Add request timeouts and retry policies.
- [ ] Add rate-limit handling and backoff.
- [ ] Preserve raw source responses.
- [ ] Record ingestion timestamps and source metadata.
- [ ] Support incremental updates.
- [ ] Make ingestion jobs safe to rerun.
- [ ] Add ingestion reports and failure summaries.

## Canonical Data Model

- [ ] Define canonical `Game` schema.
- [ ] Define canonical `Team` schema.
- [ ] Define canonical `Player` schema.
- [ ] Define canonical `TeamGame` schema.
- [ ] Define canonical `PlayerGame` schema.
- [ ] Define canonical `InjuryReport` schema.
- [ ] Define canonical `OddsSnapshot` schema.
- [ ] Define canonical `Prediction` schema.
- [ ] Define canonical `Experiment` schema.
- [ ] Define stable identifiers and entity relationships.
- [ ] Define timezone and timestamp conventions.
- [ ] Define schema versioning and migration rules.

## Temporal Data Integrity

- [ ] Define `event_time`.
- [ ] Define `available_at`.
- [ ] Define `prediction_timestamp`.
- [ ] Preserve source publication and collection timestamps where possible.
- [ ] Ensure historical features only use information available at prediction time.
- [ ] Prevent future game results from entering historical feature calculations.
- [ ] Prevent post-game statistics from leaking into pre-game predictions.
- [ ] Document how missing historical availability timestamps are handled.
- [ ] Add tests for temporal leakage.

## Storage

- [ ] Establish a partitioned Parquet dataset layout.
- [ ] Implement DuckDB query access.
- [ ] Separate raw, normalized, and derived datasets.
- [ ] Define dataset naming and versioning conventions.
- [ ] Implement data manifests and metadata.
- [ ] Verify that datasets can be reconstructed from raw snapshots.
- [ ] Establish local storage and cleanup policies.

**Exit criteria:** Historical data can be ingested, normalized, stored, queried, and reconstructed with its temporal provenance intact.

---

# M3: Data Validation and Feature Engineering

Establish trustworthy datasets before introducing complex models.

## Data Quality

- [ ] Validate required fields and data types.
- [ ] Detect duplicate records.
- [ ] Detect missing games and incomplete seasons.
- [ ] Validate team and player identifiers.
- [ ] Validate game dates and season boundaries.
- [ ] Detect impossible statistical values.
- [ ] Detect inconsistent player-team relationships.
- [ ] Validate odds formats and market identifiers.
- [ ] Detect stale and malformed odds snapshots.
- [ ] Generate dataset quality reports.
- [ ] Add automated validation tests.

## Feature Engineering

- [ ] Define a common feature interface.
- [ ] Implement rolling team statistics.
- [ ] Implement rolling player statistics.
- [ ] Implement home and away features.
- [ ] Implement rest-day features.
- [ ] Implement back-to-back game features.
- [ ] Implement schedule density and fatigue proxies.
- [ ] Implement team offensive and defensive efficiency features.
- [ ] Implement player minutes and usage features.
- [ ] Implement player availability features.
- [ ] Implement matchup features.
- [ ] Implement historical team strength features.
- [ ] Implement player and team form features.
- [ ] Implement feature normalization.
- [ ] Implement missing-value handling.
- [ ] Add feature provenance metadata.
- [ ] Add point-in-time correctness tests.
- [ ] Document feature definitions and assumptions.

## Feature Research

- [ ] Create `docs/methodology/FEATURES.md`.
- [ ] Evaluate feature usefulness independently.
- [ ] Investigate redundant and highly correlated features.
- [ ] Identify features that are unavailable in realistic prediction conditions.
- [ ] Establish feature-set versioning.

**Exit criteria:** Reproducible feature datasets can be generated without temporal leakage, and every feature has a documented definition.

---

# M4: Statistical Baselines and Forecasting

Establish simple, measurable forecasting systems before experimenting with neural networks.

## Baselines

- [ ] Implement Elo ratings for teams.
- [ ] Implement logistic regression for game outcomes.
- [ ] Implement linear regression for game-level numerical targets.
- [ ] Implement simple player-statistical baselines.
- [ ] Implement a historical average baseline.
- [ ] Implement a recent-form baseline.
- [ ] Implement XGBoost baselines.
- [ ] Implement LightGBM baselines.
- [ ] Compare baselines against simple reference predictions.
- [ ] Record baseline assumptions and limitations.

## Game Forecasting

- [ ] Define game-level prediction targets.
- [ ] Implement home-team win probability.
- [ ] Implement away-team win probability.
- [ ] Implement predicted point differential.
- [ ] Implement predicted total points.
- [ ] Investigate spread and total-market forecasting.
- [ ] Define game-level prediction output contracts.

## Player Forecasting

- [ ] Define supported player prediction targets.
- [ ] Implement minutes-played prediction.
- [ ] Implement points prediction.
- [ ] Implement rebounds prediction.
- [ ] Implement assists prediction.
- [ ] Investigate additional player statistics.
- [ ] Implement player availability-aware predictions.
- [ ] Investigate player prop market forecasting.
- [ ] Define player-level prediction output contracts.

## Model Infrastructure

- [ ] Define a common model interface.
- [ ] Define training and inference contracts.
- [ ] Implement dataset splitting and loading.
- [ ] Implement model training configuration.
- [ ] Implement checkpoint persistence.
- [ ] Implement model metadata and versioning.
- [ ] Implement prediction serialization.
- [ ] Ensure reproducible training runs.

**Exit criteria:** Game and player forecasting baselines can be trained, evaluated, saved, and reproduced.

---

# M5: Evaluation, Calibration, and Uncertainty

Build an evaluation framework that reflects how predictions would actually have been made.

## Evaluation Methodology

- [ ] Create `docs/methodology/EVALUATION.md`.
- [ ] Define chronological train, validation, and test splits.
- [ ] Implement walk-forward evaluation.
- [ ] Prevent random shuffling across temporal boundaries.
- [ ] Define season-aware evaluation.
- [ ] Define minimum sample-size requirements.
- [ ] Track model performance across time.
- [ ] Compare models against simple baselines.
- [ ] Evaluate performance across teams and player groups.
- [ ] Investigate performance degradation and distribution shifts.

## Metrics

- [ ] Implement accuracy.
- [ ] Implement log loss.
- [ ] Implement Brier score.
- [ ] Implement ROC-AUC where appropriate.
- [ ] Implement MAE.
- [ ] Implement RMSE.
- [ ] Implement calibration metrics.
- [ ] Implement prediction interval coverage.
- [ ] Generate evaluation reports.

## Calibration

- [ ] Implement reliability diagrams.
- [ ] Implement probability calibration evaluation.
- [ ] Investigate temperature scaling.
- [ ] Investigate isotonic regression.
- [ ] Compare calibrated and uncalibrated predictions.
- [ ] Evaluate calibration across different prediction groups.

## Uncertainty

- [ ] Define uncertainty output contracts.
- [ ] Investigate ensemble-based uncertainty.
- [ ] Investigate Monte Carlo dropout.
- [ ] Investigate prediction intervals.
- [ ] Evaluate uncertainty against actual forecast errors.
- [ ] Document uncertainty limitations.

**Exit criteria:** Models are evaluated chronologically, compared against baselines, and assessed for both predictive accuracy and probability calibration.

---

# M6: Market Analysis and Discrepancy Research

Compare model estimates against market-implied probabilities without turning the project into an automated betting system.

## Odds Processing

- [ ] Define canonical odds and market schemas.
- [ ] Normalize American, decimal, and fractional odds.
- [ ] Implement implied probability conversion.
- [ ] Implement no-vig probability estimation.
- [ ] Handle multiple bookmakers and market snapshots.
- [ ] Preserve bookmaker, market, selection, and timestamp metadata.
- [ ] Detect stale and inconsistent odds.
- [ ] Distinguish opening, intermediate, and closing odds.
- [ ] Define odds snapshot selection at prediction time.

## Market Comparison

- [ ] Create `docs/methodology/MARKET-ANALYSIS.md`.
- [ ] Compare model probabilities with market-implied probabilities.
- [ ] Calculate probability discrepancies.
- [ ] Calculate expected value under explicit assumptions.
- [ ] Define minimum data and confidence requirements.
- [ ] Track discrepancies across bookmakers.
- [ ] Investigate market movement.
- [ ] Compare predictions with closing-line probabilities.
- [ ] Distinguish genuine predictive edge from calibration error.
- [ ] Investigate market efficiency and model failure cases.

## Historical Simulation

- [ ] Require timestamped odds snapshots for realistic historical simulations.
- [ ] Prevent future closing odds from being used in earlier simulated decisions.
- [ ] Define paper-trading assumptions.
- [ ] Implement hypothetical stake sizing for research only.
- [ ] Track hypothetical profit and loss.
- [ ] Track ROI.
- [ ] Track maximum drawdown.
- [ ] Track closing-line value.
- [ ] Track sample size and uncertainty.
- [ ] Evaluate performance after accounting for bookmaker margins.
- [ ] Document limitations of historical odds coverage.

## Research Reporting

- [ ] Generate model-versus-market comparison reports.
- [ ] Visualize probability discrepancies.
- [ ] Visualize odds movement.
- [ ] Report historical performance by market.
- [ ] Report uncertainty and sample sizes alongside performance.
- [ ] Investigate false positives and failed predictions.

**Exit criteria:** The system can conduct reproducible, timestamp-correct market discrepancy research and paper simulations. It does not place real-money bets.

---

# M7: Experiments, Inference, and Reporting

Make experiments reproducible and results accessible.

## Experiment Tracking

- [ ] Integrate MLflow locally.
- [ ] Track model parameters.
- [ ] Track dataset and feature versions.
- [ ] Track code revision.
- [ ] Track random seeds.
- [ ] Track evaluation metrics.
- [ ] Store model artifacts.
- [ ] Compare experiments.
- [ ] Document experiment naming conventions.

## Inference

- [ ] Implement model loading.
- [ ] Implement game prediction inference.
- [ ] Implement player prediction inference.
- [ ] Validate inference inputs.
- [ ] Record prediction timestamps.
- [ ] Record model and feature versions.
- [ ] Store prediction history.
- [ ] Support reproducible historical predictions.

## Reporting

- [ ] Implement Markdown reports.
- [ ] Implement CSV exports.
- [ ] Implement Plotly visualizations.
- [ ] Generate game forecast reports.
- [ ] Generate player forecast reports.
- [ ] Generate model evaluation reports.
- [ ] Generate market discrepancy reports.
- [ ] Include uncertainty and sample sizes in reports.
- [ ] Make reports reproducible from stored experiment artifacts.

## CLI

- [ ] Establish a Typer-based CLI.
- [ ] Implement data-source inspection commands.
- [ ] Implement ingestion commands.
- [ ] Implement validation commands.
- [ ] Implement feature-generation commands.
- [ ] Implement training commands.
- [ ] Implement evaluation commands.
- [ ] Implement inference commands.
- [ ] Implement reporting commands.
- [ ] Implement experiment inspection commands.
- [ ] Add useful command help and error messages.

**Exit criteria:** The complete research workflow can be operated locally through the CLI and produces reproducible reports.

---

# M8: Advanced Research

Only pursue these after the baseline system and evaluation methodology are reliable.

## Advanced Models

- [ ] Investigate PyTorch-based game forecasting architectures.
- [ ] Investigate player-level neural forecasting architectures.
- [ ] Investigate temporal models.
- [ ] Investigate sequence-based player performance models.
- [ ] Investigate team and player interaction modeling.
- [ ] Investigate graph-based approaches.
- [ ] Investigate multi-task learning.
- [ ] Compare deep learning models against tree-based baselines.
- [ ] Measure computational cost and memory usage.
- [ ] Reject complexity that does not demonstrate measurable improvement.

## Advanced Statistical Research

- [ ] Investigate hierarchical models.
- [ ] Investigate Bayesian approaches.
- [ ] Investigate distributional forecasting.
- [ ] Investigate regime changes and concept drift.
- [ ] Investigate feature importance stability.
- [ ] Investigate model robustness under missing data.
- [ ] Investigate uncertainty-aware model selection.

## Advanced Market Research

- [ ] Investigate market-specific calibration.
- [ ] Investigate bookmaker disagreement.
- [ ] Investigate line movement patterns.
- [ ] Investigate closing-line value as an evaluation signal.
- [ ] Investigate market efficiency by market type.
- [ ] Investigate whether model discrepancies persist out of sample.

**Exit criteria:** Advanced approaches demonstrate measurable, reproducible improvements over simpler alternatives.

---

# Cross-Cutting Requirements

These requirements apply throughout the project.

## Correctness

- [ ] No temporal leakage.
- [ ] No training on information unavailable at the simulated prediction timestamp.
- [ ] No random train/test splits for time-dependent forecasting evaluation.
- [ ] No untracked manual changes to datasets.
- [ ] No undocumented assumptions in evaluation.
- [ ] No performance claims without sample sizes and uncertainty.

## Reproducibility

- [ ] Every experiment identifies its dataset version.
- [ ] Every experiment identifies its feature version.
- [ ] Every experiment identifies its code revision.
- [ ] Every experiment records its configuration and random seeds.
- [ ] Every reported metric can be reproduced from stored artifacts.

## Engineering Quality

- [ ] Keep the architecture modular without introducing unnecessary services.
- [ ] Keep external data providers replaceable.
- [ ] Keep CPU execution supported.
- [ ] Keep memory and compute requirements appropriate for local hardware.
- [ ] Add tests for critical data and temporal logic.
- [ ] Document important architectural decisions.
- [ ] Keep dependencies justified and minimal.

## Research Integrity

- [ ] Separate predictive accuracy from profitability.
- [ ] Separate historical backtest results from prospective results.
- [ ] Account for bookmaker margins.
- [ ] Do not treat closing odds as historically available information.
- [ ] Report negative and inconclusive results.
- [ ] Do not optimize against the final test set.
- [ ] Avoid presenting hypothetical paper-trading results as real-world returns.

---

# Explicitly Out of Scope

Unless a future decision changes the project scope:

- Automated real-money betting.
- Automated sportsbook account interaction.
- Production betting execution.
- Microservices.
- Kubernetes.
- Kafka or distributed event infrastructure.
- Distributed model training.
- Mandatory cloud infrastructure.
- Mandatory paid data providers.
- Complex dashboards before the research workflow is established.

---

# Definition of Done

A task is complete only when:

1. Its intended behavior is implemented or its research question is answered.
2. Relevant tests or validation checks pass.
3. Data provenance and temporal correctness are preserved where applicable.
4. Documentation reflects the actual behavior.
5. The result is reproducible.
6. The task does not silently expand the project's scope.

**Project-wide rule:** A more complex model is not automatically a better model. Evidence decides.
