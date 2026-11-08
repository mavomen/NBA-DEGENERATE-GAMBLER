# Product Requirements Document (PRD)

# NBA-DEGENERATE-GAMBLER

**Version:** 0.1.0  
**Status:** Draft  
**Project Type:** Local-first machine learning research platform  
**Primary Language:** Python  
**ML Framework:** PyTorch  
**Target Environment:** Linux  
**Development Philosophy:** Research-first, evidence-driven, reproducible

---

## 1. Executive Summary

NBA-DEGENERATE-GAMBLER is a research-oriented machine learning platform designed to forecast NBA games and individual player performances using historical basketball data, statistical methods, and deep learning.

The project has two primary objectives:

1. **Sports forecasting:** Estimate game outcomes, scores, point differentials, and individual player statistics.
2. **Market research:** Compare independently generated forecasts against sportsbook-implied probabilities to investigate potential statistical discrepancies.

The system will prioritize data quality, temporal correctness, reproducibility, probability calibration, and rigorous out-of-sample evaluation.

NBA-DEGENERATE-GAMBLER is not intended to execute real-money bets. Its market-analysis capabilities will operate through historical research and simulated paper trading.

The project will begin with statistical baselines before introducing increasingly sophisticated machine learning architectures.

**Core principle: Build the evidence first. Optimize the models second.**

---

## 2. Problem Statement

NBA games involve numerous interacting variables:

- Team performance and tactical tendencies.
- Individual player performance and availability.
- Injuries, suspensions, and lineup changes.
- Home-court advantage.
- Rest periods and schedule congestion.
- Historical matchups and opponent characteristics.
- Player workloads and changing team roles.
- Market expectations and sportsbook pricing.

Simple statistical models can capture some of these relationships but may struggle with complex temporal dependencies and interactions.

Deep learning offers additional modeling capabilities, but introduces risks such as overfitting, data leakage, excessive computational requirements, and misleading performance estimates.

NBA-DEGENERATE-GAMBLER aims to provide a structured environment in which these approaches can be developed, compared, and evaluated scientifically.

The system must answer two separate questions:

- How accurately can we forecast NBA outcomes?
- Do our forecasts contain information that differs meaningfully from available betting-market prices?

These questions must have independent evaluation pipelines.

---

## 3. Goals and Objectives

### 3.1 Primary Goals

- Build a reliable historical NBA dataset.
- Develop reproducible data ingestion and processing pipelines.
- Generate point-in-time team and player features.
- Establish statistical forecasting baselines.
- Develop deep learning models for game and player predictions.
- Produce calibrated probabilities and predictive distributions.
- Evaluate models through chronological backtesting.
- Investigate discrepancies between model forecasts and sportsbook markets.
- Maintain complete experiment provenance.

### 3.2 Secondary Goals

- Provide interpretable forecasting reports.
- Compare different model architectures.
- Investigate ensemble learning.
- Estimate prediction uncertainty.
- Support prospective forecasting and paper-trading experiments.
- Identify model degradation and data distribution changes.

### 3.3 Non-Goals

The initial project will not:

- Execute real-money bets.
- Automatically interact with sportsbook accounts.
- Guarantee profitable betting strategies.
- Depend on cloud infrastructure.
- Require distributed training.
- Require Kubernetes, Kafka, or microservices.
- Train unnecessarily large language models or Transformer architectures.
- Treat classification accuracy as evidence of profitability.

---

## 4. Target Users

### Primary User

The project developer and researcher, responsible for:

- Data engineering.
- Feature engineering.
- Statistical analysis.
- Machine learning development.
- Experiment management.
- Model evaluation.
- Market research.

### Intended Future Users

Researchers and technically proficient users interested in:

- NBA statistical forecasting.
- Sports analytics.
- Machine learning experimentation.
- Probability calibration.
- Quantitative market analysis.

The initial release is a single-user research application.

---

## 5. Core Use Cases

### UC-01: Historical Game Analysis

The user selects a historical NBA game and retrieves:

- Team statistics.
- Relevant historical features.
- Player availability information, when available.
- Model predictions.
- Actual results.
- Prediction errors.

### UC-02: Upcoming Game Forecasting

The user requests forecasts for upcoming games.

The system produces:

- Home-team win probability.
- Away-team win probability.
- Expected scores.
- Expected point differential.
- Expected total points.
- Prediction uncertainty.

Every prediction must include its generation timestamp and data provenance.

### UC-03: Player Performance Forecasting

The user requests predictions for individual players.

Initial prediction targets:

- Minutes played.
- Points.
- Rebounds.
- Assists.

The system should eventually support additional statistics through extensible prediction heads.

### UC-04: Model Comparison

The user compares multiple forecasting approaches across identical evaluation periods.

The system reports:

- Predictive performance.
- Calibration.
- Prediction uncertainty.
- Computational cost.
- Differences from baseline models.

### UC-05: Market Discrepancy Research

The user compares model-generated probabilities with sportsbook-implied probabilities.

The system calculates:

- Raw implied probabilities.
- No-vig probabilities.
- Model-market probability differences.
- Expected value estimates under explicit assumptions.
- Historical simulated returns.
- Maximum drawdown.
- Closing-line value (CLV), where suitable timestamped data exists.

### UC-06: Experiment Reproduction

The user selects a previous experiment and reproduces it using its recorded:

- Dataset version.
- Git commit.
- Feature configuration.
- Model configuration.
- Random seed.
- Training parameters.
- Evaluation period.

---

## 6. Functional Requirements

Requirements are prioritized as follows:

- **P0:** Required for the initial usable release.
- **P1:** Required for the complete forecasting platform.
- **P2:** Advanced or optional research capabilities.

### 6.1 Data Ingestion

The system must:

- Support NBA historical data ingestion.
- Provide replaceable source adapters.
- Retrieve game results and box scores.
- Retrieve team and player statistics.
- Support incremental data updates.
- Preserve raw source snapshots.
- Record source provenance.
- Handle retries, timeouts, and rate limits.
- Detect duplicate records.
- Validate downloaded data.
- Document source coverage and limitations.

Initial source candidates:

- NBA Stats through `nba_api`.
- Public historical datasets.
- ESPN supplementary endpoints.
- Sportsbook odds providers.
- Official NBA injury reports.

No source should be assumed permanently reliable or freely accessible.

### 6.2 Data Management

The system must:

- Maintain canonical game, team, player, and player-game schemas.
- Normalize inconsistent source formats.
- Preserve historical team and player associations.
- Support missing-value analysis.
- Validate data types and constraints.
- Store processed data in Parquet.
- Support analytical queries through DuckDB.
- Avoid loading entire historical datasets into memory.

Every relevant record must preserve temporal information.

Required timestamps:

| Field                  | Description                           |
| ---------------------- | ------------------------------------- |
| `event_time`           | When the real-world event occurred    |
| `available_at`         | When the information became available |
| `prediction_timestamp` | When the forecast was generated       |

These fields are essential for preventing look-ahead bias.

### 6.3 Feature Engineering

The system must support reusable, configurable feature pipelines.

**Team features**

- Offensive Rating.
- Defensive Rating.
- Net Rating.
- Pace.
- Effective Field Goal Percentage.
- True Shooting Percentage.
- Turnover Percentage.
- Rebounding Percentage.
- Free Throw Rate.

**Temporal features**

- Rolling averages over 3, 5, 10, and 15 games.
- Exponentially weighted moving averages.
- Season-to-date statistics.
- Recent performance trends.
- Historical performance volatility.

**Schedule features**

- Home/away status.
- Rest days.
- Back-to-back games.
- Consecutive road games.
- Schedule congestion.
- Travel distance, when reliable data is available.

**Player features**

- Minutes played.
- Usage rate.
- Points.
- Rebounds.
- Assists.
- Shooting efficiency.
- Recent workload.
- Availability and expected role.

**Matchup features**

- Offensive and defensive differences.
- Rebounding mismatches.
- Pace differences.
- Player availability effects.
- Historical matchup statistics.

All features must be computed using information available at the prediction timestamp.

### 6.4 Game Forecasting

**P0 requirements**

The initial game forecasting pipeline must:

- Accept historical team and matchup features.
- Generate home-team and away-team win probabilities.
- Generate expected home and away scores.
- Generate expected point differential.
- Generate expected total points.
- Persist predictions and their metadata.

**P1 requirements**

The forecasting pipeline should:

- Generate predictive distributions.
- Estimate uncertainty.
- Support multiple model architectures.
- Support model ensembles.
- Provide feature importance or interpretability reports.

### 6.5 Player Forecasting

**P1 requirements**

The player forecasting pipeline must:

- Support historical player statistics.
- Account for player roles and team membership.
- Model expected playing time.
- Forecast minutes, points, rebounds, and assists.
- Produce predictive distributions.
- Account for teammate availability when data permits.
- Support historical player-team associations.

Expected minutes should be treated as an important intermediate prediction because player statistics depend heavily on playing time.

### 6.6 Statistical Baselines

The system must implement:

- Historical home-court baseline.
- Elo ratings.
- Logistic regression.
- Linear regression.
- XGBoost.
- LightGBM.

Baselines are mandatory comparison points for every more sophisticated model.

### 6.7 Deep Learning

The system should support:

**Game forecasting**

- Multilayer Perceptron (MLP).
- GRU-based temporal encoder.
- LSTM-based temporal encoder.
- Shared multi-task architectures.

Potential output heads:

- Win probability.
- Home score.
- Away score.
- Point differential.
- Total points.

**Player forecasting**

- Player feature encoder.
- Temporal sequence encoder.
- Context encoder.
- Minutes prediction head.
- Points prediction head.
- Rebounds prediction head.
- Assists prediction head.

Transformers and Graph Neural Networks are experimental extensions, not initial requirements.

### 6.8 Training

The training system must:

- Support configurable hyperparameters.
- Support deterministic random seeds where practical.
- Support CPU execution.
- Support CUDA when compatible.
- Support checkpoint saving and recovery.
- Support configurable batch sizes.
- Record training duration.
- Record dataset and feature versions.
- Support multiple experiments without configuration conflicts.

### 6.9 Evaluation

The evaluation system must support chronological and walk-forward validation.

**Classification metrics**

- Accuracy.
- Precision.
- Recall.
- F1.
- ROC-AUC.
- Log Loss.
- Brier Score.
- Expected Calibration Error (ECE).

**Regression metrics**

- MAE.
- RMSE.
- R².
- Prediction interval coverage.

**Market research metrics**

- No-vig probability comparison.
- Expected value.
- ROI.
- Maximum drawdown.
- Closing-line value.
- Sample size.
- Confidence intervals and uncertainty estimates.

Randomly splitting individual games across training and testing is prohibited for primary performance claims.

Calibration must be fitted using validation data, never the final test set.

### 6.10 Probability Calibration and Uncertainty

The system should support:

- Temperature scaling.
- Isotonic regression.
- Reliability diagrams.
- Calibration reports.
- Prediction intervals.
- Ensemble variance.
- Monte Carlo dropout where appropriate.

Forecasts must not be presented as certain outcomes.

### 6.11 Market Analysis

The market module must:

- Import historical sportsbook odds.
- Preserve bookmaker identity.
- Preserve odds timestamps.
- Convert odds into implied probabilities.
- Calculate no-vig probabilities.
- Compare market probabilities with model predictions.
- Estimate expected value under documented assumptions.
- Simulate historical paper-trading strategies.
- Report ROI, drawdown, and CLV when data permits.

The market module must remain logically separate from the initial forecasting model.

Historical closing odds must not be treated as prices available earlier in the day. Strategy evaluation requires timestamped odds snapshots corresponding to the simulated decision time.

### 6.12 Experiment Tracking

Every experiment must record:

- Experiment ID.
- Git commit.
- Dataset version.
- Feature configuration.
- Model architecture.
- Hyperparameters.
- Random seed.
- Training duration.
- Evaluation period.
- Metrics.
- Checkpoint location.
- Research notes.

MLflow will be used for experiment tracking.

Negative results must be preserved.

### 6.13 Reporting

The system must generate:

- Dataset quality reports.
- Data coverage reports.
- Model comparison reports.
- Training reports.
- Evaluation reports.
- Calibration reports.
- Market analysis reports.

Initial output formats:

- Markdown.
- CSV.
- Interactive Plotly visualizations.

### 6.14 CLI

The application should provide a unified command-line interface using Typer.

Expected command groups:

```text
nba-oracle data
nba-oracle features
nba-oracle train
nba-oracle evaluate
nba-oracle predict
nba-oracle market
nba-oracle experiments
nba-oracle report
```

Exact commands and arguments will be defined during implementation.

---

## 7. Technical Requirements

### 7.1 Technology Stack

| Component           | Technology        |
| ------------------- | ----------------- |
| Language            | Python 3.12+      |
| Deep Learning       | PyTorch           |
| Numerical Computing | NumPy             |
| Data Processing     | Polars, Pandas    |
| Traditional ML      | scikit-learn      |
| Gradient Boosting   | XGBoost, LightGBM |
| Storage             | Parquet           |
| Analytical Database | DuckDB            |
| Experiment Tracking | MLflow            |
| Configuration       | YAML, Pydantic    |
| Visualization       | Plotly            |
| Exploration         | Jupyter           |
| CLI                 | Typer             |
| Testing             | pytest            |
| Package Management  | uv                |
| Version Control     | Git               |

Dependencies must be pinned through a lockfile.

### 7.2 Architecture

NBA-DEGENERATE-GAMBLER will use a modular monolithic architecture.

Major components:

1. Data ingestion.
2. Data normalization and validation.
3. Data storage.
4. Feature engineering.
5. Statistical baselines.
6. Model training.
7. Game forecasting.
8. Player forecasting.
9. Evaluation and calibration.
10. Market research.
11. Experiment tracking.
12. Reporting and CLI.

Modules should expose clear interfaces and avoid unnecessary coupling.

### 7.3 Hardware Constraints

The project must operate locally.

Initial hardware target:

- NVIDIA GTX 1650.
- 16 GB system RAM.
- Linux environment.
- CPU-only fallback.

Models must remain appropriately sized for this hardware.

The system should:

- Support batch processing.
- Avoid unnecessary data duplication.
- Use efficient columnar storage.
- Support CPU training and inference.
- Avoid requiring large GPU memory.
- Allow model size and sequence length to be configured.

### 7.4 Deployment

Initial deployment is local-only.

Docker may be introduced later for reproducibility, but must not become a prerequisite for development.

Cloud services and distributed infrastructure are explicitly excluded from the initial architecture.

---

## 8. Data Requirements and Constraints

### 8.1 Historical Coverage

The project should investigate available coverage for:

| Dataset                      | Priority |
| ---------------------------- | -------- |
| Game results                 | P0       |
| Game box scores              | P0       |
| Team statistics              | P0       |
| Player statistics            | P0       |
| Play-by-play                 | P1       |
| Historical injuries          | P1       |
| Timestamped sportsbook odds  | P1       |
| Player prop odds             | P2       |
| Advanced tracking statistics | P2       |

### 8.2 Data Provenance

Every dataset must document:

- Source.
- Retrieval date.
- Historical coverage.
- Update frequency.
- Known limitations.
- Licensing restrictions.
- Data quality issues.

### 8.3 Historical Availability

A major limitation is that historical data does not necessarily represent what was known before each game.

For example:

- Current player statistics may include corrections made after a game.
- Historical injury reports may be incomplete.
- Final odds may not reflect prices available hours earlier.
- Historical team rosters may differ from current rosters.

The system must document these limitations and avoid making unsupported claims about historical forecasting conditions.

Prospective injury and odds snapshots should be collected with timestamps whenever possible.

---

## 9. Scientific Methodology

Scientific validity is a core product requirement.

### 9.1 Chronological Evaluation

Data must be split chronologically.

An illustrative initial split:

- Training: 2010–2022.
- Validation: 2023.
- Testing: 2024.
- Prospective evaluation: 2025 onward.

Actual periods depend on available and validated data.

### 9.2 Walk-Forward Backtesting

The evaluation pipeline must:

1. Select a historical prediction date.
2. Load only information available at that date.
3. Construct point-in-time features.
4. Train or update the model according to the experiment configuration.
5. Generate predictions.
6. Persist predictions before outcomes are incorporated.
7. Evaluate predictions after results become available.
8. Repeat across the evaluation period.

### 9.3 Leakage Prevention

The system must prevent:

- Future game statistics entering historical features.
- Future injury information entering predictions.
- Future odds entering market simulations.
- Random train/test contamination.
- Post-game data entering pre-game forecasts.
- Calibration using final test outcomes.

Automated leakage tests are required.

### 9.4 Model Complexity

A more complex architecture must demonstrate meaningful out-of-sample improvement over simpler baselines.

Model complexity alone is not a measure of progress.

### 9.5 Market Research Discipline

Market results must account for:

- Betting margins.
- Odds availability.
- Execution assumptions.
- Market timing.
- Sample size.
- Statistical uncertainty.
- Multiple strategy comparisons.
- Potential selection bias.

A positive historical ROI on a small sample must never be presented as proof of a profitable strategy.

---

## 10. Repository Structure

The proposed repository structure:

```text
nba-oracle/
├── configs/
│   ├── data/
│   ├── features/
│   ├── models/
│   ├── experiments/
│   └── evaluation/
│
├── data/
│   ├── raw/
│   ├── processed/
│   ├── features/
│   └── metadata/
│
├── notebooks/
│   ├── exploration/
│   ├── analysis/
│   └── research/
│
├── experiments/
│   └── results/
│
├── models/
│   ├── checkpoints/
│   └── artifacts/
│
├── reports/
│   ├── datasets/
│   ├── experiments/
│   ├── calibration/
│   └── market/
│
├── src/
│   └── nba_oracle/
│       ├── ingestion/
│       │   ├── sources/
│       │   ├── adapters/
│       │   └── collectors/
│       │
│       ├── data/
│       │   ├── schemas/
│       │   ├── validation/
│       │   ├── normalization/
│       │   └── storage/
│       │
│       ├── features/
│       │   ├── team/
│       │   ├── player/
│       │   ├── temporal/
│       │   ├── matchup/
│       │   └── pipelines/
│       │
│       ├── baselines/
│       ├── models/
│       │   ├── game/
│       │   ├── player/
│       │   ├── encoders/
│       │   ├── heads/
│       │   └── ensembles/
│       │
│       ├── training/
│       ├── evaluation/
│       ├── calibration/
│       ├── uncertainty/
│       ├── market/
│       ├── experiments/
│       ├── inference/
│       ├── reporting/
│       ├── cli/
│       └── common/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── data/
│   └── research/
│
├── docs/
│   ├── architecture/
│   ├── methodology/
│   ├── datasets/
│   └── decisions/
│
├── scripts/
│
├── pyproject.toml
├── uv.lock
├── README.md
├── PRD.md
├── FEATURE-LIST.md
├── ARCHITECTURE.md
├── CONTRIBUTING.md
├── LICENSE
└── .gitignore
```

Large datasets, model checkpoints, and generated experiment artifacts must not be committed to Git.

---

## 11. Development Roadmap

### M0: Research Foundation

Objectives:

- Investigate historical NBA data sources.
- Build a dataset coverage matrix.
- Define canonical data schemas.
- Implement initial source adapters.
- Download historical game results and box scores.
- Validate data quality.
- Document source limitations.

**Deliverable:** A validated historical dataset with documented provenance and coverage.

### M1: Statistical Baselines

Objectives:

- Implement Elo ratings.
- Implement logistic regression.
- Implement linear regression.
- Implement XGBoost and LightGBM baselines.
- Build chronological evaluation.
- Generate initial performance reports.

**Deliverable:** Reproducible baseline forecasting results.

### M2: Game Forecasting

Objectives:

- Implement team feature pipelines.
- Build MLP game forecasting.
- Experiment with GRU and LSTM encoders.
- Implement multi-task prediction.
- Compare deep learning against baselines.

**Deliverable:** Evaluated game forecasting models.

### M3: Player Forecasting

Objectives:

- Implement player feature pipelines.
- Model expected minutes.
- Forecast points, rebounds, and assists.
- Evaluate player-level prediction distributions.

**Deliverable:** Initial player performance forecasting pipeline.

### M4: Advanced Research

Objectives:

- Implement probability calibration.
- Estimate predictive uncertainty.
- Experiment with ensembles.
- Investigate model interpretability.
- Perform feature ablation studies.

**Deliverable:** Calibrated forecasts and documented research findings.

### M5: Market Research

Objectives:

- Integrate historical sportsbook odds.
- Calculate implied and no-vig probabilities.
- Compare model and market probabilities.
- Implement paper-trading simulations.
- Analyze ROI, drawdown, and CLV.
- Document statistical uncertainty.

**Deliverable:** Reproducible market discrepancy research.

### M6: Forecasting Interface

Objectives:

- Implement unified CLI.
- Support historical game queries.
- Support upcoming game predictions.
- Support player predictions.
- Persist prediction history.
- Generate reports and visualizations.

**Deliverable:** A usable local forecasting application.

---

## 12. Non-Functional Requirements

### Performance

- Process historical datasets without requiring full in-memory loading.
- Support configurable training batch sizes.
- Use columnar storage.
- Avoid unnecessary recomputation.
- Provide reasonable CPU-only execution.

### Reliability

- Validate external data.
- Handle source failures gracefully.
- Preserve raw data snapshots.
- Support interrupted training recovery.
- Detect corrupted or incomplete datasets.

### Maintainability

- Use typed public interfaces.
- Separate domain logic from infrastructure.
- Keep configuration external to model implementations.
- Document architectural decisions.
- Maintain automated tests.

### Reproducibility

- Track dataset versions.
- Track Git commits.
- Track experiment configurations.
- Record random seeds.
- Preserve model checkpoints and metrics.

### Portability

- Linux-first.
- CPU-compatible.
- CUDA support when available.
- No mandatory cloud services.

---

## 13. Testing Requirements

### Unit Tests

- Feature calculations.
- Statistical transformations.
- Probability calculations.
- Odds conversion.
- Data normalization.
- Model output validation.

### Integration Tests

- Data ingestion.
- Storage operations.
- Feature pipelines.
- Training workflows.
- Prediction workflows.
- Experiment tracking.

### Data Tests

- Duplicate detection.
- Missing-value validation.
- Schema validation.
- Referential integrity.
- Temporal consistency.
- Historical team/player association.

### Research Tests

- Chronological split validation.
- Leakage prevention.
- Calibration separation.
- Prediction timestamp validation.
- Reproducibility checks.

A model that trains successfully but violates temporal correctness is considered broken.

---

## 14. Risks and Mitigations

| Risk                                 | Mitigation                                             |
| ------------------------------------ | ------------------------------------------------------ |
| NBA endpoints become unreliable      | Multiple replaceable data adapters                     |
| Historical injury data is incomplete | Prospective timestamped collection                     |
| Data leakage                         | Point-in-time feature construction and automated tests |
| Small effective sample size          | Season-based evaluation and uncertainty reporting      |
| Model overfitting                    | Walk-forward validation and baseline comparisons       |
| Limited GPU memory                   | Compact models and configurable batches                |
| Historical odds limitations          | Coverage documentation and source comparison           |
| Misleading profitability claims      | Paper trading and statistical uncertainty              |
| Model degradation                    | Prospective monitoring                                 |
| Dependency instability               | Lockfiles and compatibility tests                      |
| Data licensing restrictions          | Source and license review before redistribution        |

---

## 15. Acceptance Criteria: v0.1.0

The first usable release is complete when:

1. Historical NBA game data can be ingested reproducibly.
2. Canonical data schemas are implemented and validated.
3. Historical team features can be generated.
4. Elo ratings are implemented.
5. Logistic regression forecasting works.
6. At least one gradient boosting baseline works.
7. A PyTorch MLP can be trained.
8. A PyTorch GRU can be trained.
9. Game win probabilities can be generated.
10. Expected score estimates can be generated.
11. Chronological backtesting works.
12. Log Loss and Brier Score are reported.
13. Experiments are reproducible from configuration files.
14. Leakage tests pass.
15. The application runs locally.
16. Results can be exported to Markdown and CSV.
17. Dataset limitations and evaluation methodology are documented.

Player forecasting, market analysis, and advanced calibration are subsequent milestones. They must not be falsely represented as completed v0.1.0 capabilities.

---

## 16. Definition of Done

NBA-DEGENERATE-GAMBLER v0.1.0 is considered complete when it has:

- A reliable historical game dataset.
- A validated data pipeline.
- A reproducible feature engineering pipeline.
- Statistical forecasting benchmarks.
- Initial neural forecasting models.
- Chronological evaluation.
- Documented research methodology.
- Automated leakage tests.
- Reproducible experiment configurations.
- Local execution and reporting.

A successful release does not require outperforming sportsbook markets.

It requires a trustworthy foundation on which such a hypothesis can be investigated.

---

## 17. Guiding Principles

1. Data quality outranks model complexity.
2. Neural networks are not automatically better than statistical models.
3. Every forecast must respect information availability.
4. Probabilities must be evaluated for calibration.
5. Uncertainty must be reported.
6. Historical evaluation must be chronological.
7. Experiments must be reproducible.
8. Negative results must be preserved.
9. Predictive accuracy does not imply profitability.
10. No real-money execution is within project scope.

---

**Final Principle**

Build the evidence first. Optimize the models second. Never confuse a convincing backtest with a reliable forecasting system.
