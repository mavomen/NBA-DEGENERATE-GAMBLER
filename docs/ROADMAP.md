# ROADMAP

> **Project:** NBA Degenerate Gambler  
> **Category:** Applied Machine Learning, Sports Analytics, Predictive Modeling  
> **Development philosophy:** Research-first, evidence-driven, local-first  
> **Primary objective:** Build a reproducible NBA forecasting and market-discrepancy research platform that demonstrates practical machine learning competence.

---

## 1. Vision

NBA Degenerate Gambler is a research-oriented machine learning project focused on predicting NBA game outcomes and player performance, evaluating predictive uncertainty, and investigating discrepancies between model estimates and betting market probabilities.

The project is designed to demonstrate competence across the complete applied ML lifecycle:

1. Data discovery and acquisition.
2. Data engineering and temporal integrity.
3. Exploratory data analysis.
4. Statistical analysis and feature engineering.
5. Baseline modeling.
6. Supervised machine learning.
7. Deep learning experimentation.
8. Model evaluation and calibration.
9. Experiment tracking and reproducibility.
10. Inference and prediction reporting.
11. Statistical comparison against external market estimates.

The objective is not to produce the most complicated model possible.

The objective is to demonstrate that every modeling decision is supported by evidence, every experiment is reproducible, and every reported result survives rigorous evaluation.

## 2. Guiding Principles

### Evidence over complexity

- Establish statistical baselines before implementing neural networks.
- Compare every advanced model against simpler alternatives.
- Reject complexity that does not produce measurable improvements.
- Preserve unsuccessful experiments and document what they taught us.

### Temporal correctness

- Respect the information available at the time of each prediction.
- Prevent future information from leaking into historical features.
- Use chronological evaluation rather than random splits.
- Distinguish event timestamps, data availability timestamps, and prediction timestamps.

### Reproducibility

- Version datasets and feature definitions.
- Track experiment configurations and random seeds.
- Record model versions and source revisions.
- Preserve evaluation artifacts.
- Make reported results independently reproducible.

### Scientific honesty

- Report limitations, uncertainty, and sample sizes.
- Distinguish predictive accuracy from hypothetical profitability.
- Avoid cherry-picked evaluation periods.
- Separate exploratory research from final testing.
- Never present backtest performance as proof of future profitability.

### Engineering discipline

- Keep the system modular and maintainable.
- Support local CPU execution and optional CUDA acceleration.
- Prefer simple infrastructure.
- Keep data providers replaceable.
- Make research workflows executable through a consistent interface.

---

## 3. Development Phases

The roadmap is organized into nine phases. Each phase has a specific purpose, tangible deliverables, and evidence of completion.

Progress should be measured by verified deliverables, not by the number of completed checkboxes.

---

## Phase 0: Engineering Foundation

<badge color="success">Foundation</badge> <badge>Priority: Critical</badge>

**Objective:** Establish a reproducible development environment and a maintainable project structure.

### Work

- Establish the Python development environment.
- Configure dependency management with `uv`.
- Configure Ruff and pytest.
- Establish project configuration using YAML and Pydantic.
- Define repository architecture and module boundaries.
- Establish logging and error-handling conventions.
- Configure automated quality checks.
- Establish experiment and dataset directory conventions.
- Document architectural decisions.

### Deliverables

- Reproducible development environment.
- `pyproject.toml`.
- `Makefile`.
- `.editorconfig`.
- `AGENTS.md`.
- `ARCHITECTURE.md`.
- `FEATURE-LIST.md`.
- Automated quality-check workflow.
- Documented development conventions.

### Evidence of competence

- Reproducible Python environment.
- Modular software architecture.
- Dependency and configuration management.
- Automated testing and code quality.
- Engineering documentation.

### Exit criteria

A fresh checkout can be configured and validated without undocumented machine-specific dependencies.

---

## Phase 1: Data Research and Acquisition

<badge>Priority: Critical</badge>

**Objective:** Establish a trustworthy historical and prospective NBA dataset.

### Work

- Investigate available NBA data sources.
- Evaluate historical game and player statistics.
- Investigate team-level performance data.
- Investigate injuries and player availability.
- Investigate schedules and game metadata.
- Investigate historical betting odds.
- Evaluate data coverage and licensing.
- Implement replaceable source adapters.
- Preserve raw source responses.
- Build ingestion and validation workflows.

### Deliverables

- Documented data-source inventory.
- Dataset coverage matrix.
- Raw data collection pipeline.
- Canonical data schemas.
- Historical game dataset.
- Historical player dataset.
- Data quality reports.
- Source limitations documentation.

### Evidence of competence

- Data acquisition and integration.
- API consumption and source abstraction.
- Data cleaning and normalization.
- Schema design.
- Data quality assessment.
- Data provenance and lineage.

### Exit criteria

The project can collect and validate its initial historical dataset, explain its limitations, and reproduce its ingestion process.

---

## Phase 2: Exploratory Data Analysis and Statistical Research

<badge>Priority: Critical</badge>

**Objective:** Understand the underlying data before making modeling decisions.

### Work

- Investigate game outcome distributions.
- Analyze team offensive and defensive performance.
- Investigate home-court advantage.
- Analyze rest days and schedule density.
- Investigate player minutes and usage distributions.
- Analyze player performance variability.
- Investigate relationships between player and team statistics.
- Analyze missingness and outliers.
- Investigate season-to-season distribution changes.
- Identify potential sources of bias.
- Establish initial statistical hypotheses.

### Deliverables

- Reproducible EDA notebooks.
- Statistical summaries.
- Distribution visualizations.
- Correlation analyses.
- Data quality findings.
- Documented research hypotheses.
- EDA report.

### Evidence of competence

- Exploratory data analysis.
- Descriptive and inferential statistics.
- Statistical reasoning.
- Distribution analysis.
- Data visualization.
- Hypothesis formulation.
- Identification of data quality problems.

### Exit criteria

The project has documented statistical findings that inform feature engineering and model selection.

---

## Phase 3: Feature Engineering and Baseline Models

<badge>Priority: Critical</badge>

**Objective:** Establish interpretable features and statistically defensible reference models.

### Work

- Define point-in-time feature generation.
- Implement rolling team statistics.
- Implement rolling player statistics.
- Implement home/away features.
- Implement rest and schedule features.
- Implement offensive and defensive efficiency features.
- Implement player availability features.
- Implement matchup features.
- Implement feature normalization and missing-value handling.
- Establish historical and statistical baselines.
- Implement Elo ratings.
- Implement logistic regression.
- Implement linear regression.
- Implement simple player-statistical predictors.

### Deliverables

- Feature engineering pipeline.
- Versioned feature datasets.
- Feature documentation.
- Baseline model implementations.
- Baseline evaluation reports.
- Temporal leakage tests.

### Evidence of competence

- Feature engineering.
- Statistical modeling.
- Supervised learning fundamentals.
- Regression and classification.
- Data leakage prevention.
- Model comparison.
- Interpretability.

### Exit criteria

Every initial forecasting task has at least one simple, reproducible baseline and a documented evaluation result.

---

## Phase 4: Applied Machine Learning

<badge>Priority: Critical</badge>

**Objective:** Develop and compare practical machine learning models for NBA forecasting.

### Game forecasting

- Predict game outcome probabilities.
- Predict point differentials.
- Predict total points.
- Investigate spread and totals forecasting.

### Player forecasting

- Predict player minutes.
- Predict player points.
- Predict rebounds.
- Predict assists.
- Investigate additional player statistics.
- Incorporate availability and matchup information.

### Models

- Logistic regression.
- Linear and regularized regression.
- Random Forest where appropriate.
- XGBoost.
- LightGBM.
- Other justified tree-based models.

### Research

- Compare feature sets.
- Investigate model complexity.
- Evaluate feature importance.
- Investigate interactions between variables.
- Compare performance across seasons.
- Investigate model stability.
- Analyze errors and failure cases.

### Deliverables

- Reusable model interfaces.
- Training pipelines.
- Model checkpoints.
- Model comparison reports.
- Feature importance reports.
- Error analysis reports.
- Reproducible experiment configurations.

### Evidence of competence

- Practical supervised machine learning.
- Classification and regression.
- Gradient boosting.
- Hyperparameter optimization.
- Feature selection.
- Model diagnostics.
- Error analysis.
- Model comparison.

### Exit criteria

The project has multiple evaluated ML models, with clear evidence explaining which approaches work, which do not, and why.

---

## Phase 5: Evaluation, Calibration, and Uncertainty

<badge>Priority: Critical</badge>

**Objective:** Establish whether model predictions are reliable, not merely whether their average errors look attractive.

### Work

- Implement chronological train/validation/test splits.
- Implement walk-forward evaluation.
- Evaluate across multiple seasons.
- Implement classification and regression metrics.
- Evaluate probability calibration.
- Implement reliability diagrams.
- Investigate temperature scaling.
- Investigate isotonic regression.
- Investigate ensemble uncertainty.
- Investigate prediction intervals.
- Evaluate model degradation over time.
- Investigate distribution shifts.
- Compare models against baselines.

### Metrics

Classification:

- Accuracy.
- Log loss.
- Brier score.
- ROC-AUC where appropriate.
- Calibration error.

Regression:

- MAE.
- RMSE.
- Prediction interval coverage.

Additional evaluation:

- Performance by season.
- Performance by team.
- Performance by player group.
- Calibration by probability range.
- Error distribution.
- Stability across evaluation windows.

### Deliverables

- Walk-forward evaluation framework.
- Model evaluation reports.
- Calibration reports.
- Reliability diagrams.
- Uncertainty analysis.
- Error analysis.
- Model comparison dashboards or reports.

### Evidence of competence

- Experimental design.
- Time-series-aware validation.
- Statistical evaluation.
- Probability calibration.
- Uncertainty quantification.
- Model reliability analysis.
- Generalization assessment.

### Exit criteria

Model quality is evaluated across time, with predictive performance, calibration, uncertainty, and failure cases documented.

---

## Phase 6: Deep Learning Research

<badge>Priority: High</badge>

**Objective:** Investigate whether neural architectures provide measurable improvements over statistical and tree-based models.

This phase deliberately follows baseline and applied ML development.

### Work

- Establish a PyTorch training workflow.
- Implement reproducible training loops.
- Investigate neural networks for game forecasting.
- Investigate neural networks for player forecasting.
- Investigate temporal architectures.
- Investigate sequence-based player performance models.
- Investigate team/player interaction representations.
- Investigate multi-task learning.
- Investigate graph-based approaches where justified.
- Evaluate regularization and optimization strategies.
- Compare neural models against tree-based baselines.
- Measure training cost and inference performance.

### Deliverables

- PyTorch training infrastructure.
- Neural model implementations.
- Training and validation logs.
- Checkpoints and experiment metadata.
- Architecture comparison reports.
- Deep learning research notes.

### Evidence of competence

- PyTorch.
- Neural network architecture design.
- Optimization and regularization.
- Training-loop implementation.
- GPU and CPU execution.
- Model checkpointing.
- Deep learning evaluation.
- Experimental comparison.

### Exit criteria

At least one neural architecture has been rigorously compared against simpler models. A neural model does not need to win for this phase to be successful.

A well-documented negative result is valid research.

---

## Phase 7: Market Discrepancy Research

<badge>Priority: High</badge>

**Objective:** Investigate whether model estimates reveal statistically meaningful discrepancies against betting market probabilities.

This is a research and paper-simulation module, not an automated betting system.

### Work

- Normalize bookmaker odds.
- Convert odds to implied probabilities.
- Implement no-vig probability estimation.
- Compare model probabilities against market probabilities.
- Investigate market movement.
- Compare bookmaker estimates.
- Evaluate market discrepancies.
- Implement hypothetical expected-value calculations.
- Implement paper-trading simulations.
- Track ROI and drawdown.
- Investigate closing-line value.
- Evaluate results across market types.
- Account for uncertainty and bookmaker margins.

### Critical constraint

Historical market evaluation must use odds snapshots that would have been available at the simulated prediction time.

Historical closing odds must not be treated as information available before the game.

### Deliverables

- Odds normalization pipeline.
- Market probability calculations.
- Model-versus-market comparisons.
- Historical market analysis reports.
- Paper-trading simulator.
- ROI, drawdown, and CLV reports.
- Market research documentation.

### Evidence of competence

- Probability theory.
- Statistical decision analysis.
- Expected-value calculations.
- Financial-style performance metrics.
- Historical simulation.
- Bias and leakage prevention.
- Evaluation under uncertainty.

### Exit criteria

The project can reproduce market discrepancy research using timestamp-correct odds and clearly documented simulation assumptions.

---

## Phase 8: Experiment Management and Inference

<badge>Priority: High</badge>

**Objective:** Turn the research components into a coherent, reproducible local ML workflow.

### Work

- Integrate local MLflow tracking.
- Record model parameters and metrics.
- Record dataset and feature versions.
- Record code revisions and random seeds.
- Store model artifacts.
- Implement model loading.
- Implement game inference.
- Implement player inference.
- Store prediction history.
- Generate reports.
- Establish a Typer CLI.
- Support reproducible historical predictions.

### Deliverables

- Local experiment tracking.
- Model registry or equivalent artifact organization.
- Inference interfaces.
- Prediction history.
- CLI commands.
- Markdown and CSV reports.
- Plotly visualizations.
- Reproducibility documentation.

### Evidence of competence

- ML experiment management.
- Model artifact management.
- Inference pipelines.
- Reproducibility.
- ML tooling.
- CLI development.
- Reporting and communication.

### Exit criteria

A complete local workflow can ingest data, generate features, train models, evaluate experiments, perform inference, and produce reproducible reports.

---

## 4. Portfolio Milestones

The phases above describe technical development. These milestones describe what an external reviewer should be able to inspect.

| Milestone | Portfolio evidence | What it demonstrates |
|---|---|---|
| P1: Data Foundation | Data pipeline, schemas, coverage report | Data engineering |
| P2: Statistical Research | EDA notebooks and research report | Statistics and analytical thinking |
| P3: Baselines | Reproducible baseline models | ML fundamentals |
| P4: Applied ML | XGBoost/LightGBM model comparisons | Practical ML |
| P5: Evaluation | Walk-forward and calibration reports | Scientific evaluation |
| P6: Deep Learning | PyTorch experiments | Neural network development |
| P7: Market Research | Timestamp-correct market analysis | Applied probability and decision analysis |
| P8: Research Platform | MLflow, CLI, inference, reproducibility | ML engineering |

A portfolio milestone is complete only when its deliverables are present, executable, and documented.

---

## 5. Required Portfolio Artifacts

The following artifacts should be maintained as first-class project outputs.

### Research documentation

- `docs/datasets/COVERAGE.md`
- `docs/methodology/EDA.md`
- `docs/methodology/FEATURES.md`
- `docs/methodology/EVALUATION.md`
- `docs/methodology/MODEL-COMPARISON.md`
- `docs/methodology/CALIBRATION.md`
- `docs/methodology/MARKET-ANALYSIS.md`
- `docs/methodology/EXPERIMENTS.md`

### Research notebooks

- Data quality investigation.
- Exploratory game analysis.
- Exploratory player analysis.
- Team performance analysis.
- Player performance analysis.
- Feature engineering experiments.
- Baseline model evaluation.
- Tree-based model comparison.
- Deep learning experiments.
- Calibration and uncertainty analysis.
- Market discrepancy analysis.

Notebooks should support exploration, not become the only place where production logic exists. Reusable logic belongs in the project modules.

### Model artifacts

- Baseline model checkpoints.
- Trained model checkpoints.
- Model configuration files.
- Feature definitions.
- Evaluation reports.
- Calibration reports.
- Experiment metadata.
- Reproducible prediction examples.

### Demonstrations

- Game prediction example.
- Player prediction example.
- Model-versus-market comparison.
- Historical walk-forward evaluation.
- Experiment comparison.
- Reproducible CLI workflow.

---

## 6. Research Quality Gates

Before claiming a model or experiment is successful, verify the following.

### Data

- [ ] Source and coverage are documented.
- [ ] Dataset version is identifiable.
- [ ] Missing data is understood.
- [ ] Temporal availability is respected.
- [ ] No future information enters historical features.

### Modeling

- [ ] A simple baseline exists.
- [ ] Training and evaluation periods are separated.
- [ ] Hyperparameter tuning does not use the final test set.
- [ ] Model configuration is recorded.
- [ ] Random seeds are recorded where applicable.

### Evaluation

- [ ] Evaluation is chronological.
- [ ] Metrics are appropriate for the prediction target.
- [ ] Sample sizes are reported.
- [ ] Calibration is assessed for probability predictions.
- [ ] Error cases are investigated.
- [ ] Results are compared against a baseline.
- [ ] Limitations are documented.

### Reproducibility

- [ ] The experiment can be rerun.
- [ ] Dataset and feature versions are recorded.
- [ ] Code revision is recorded.
- [ ] Model artifacts are preserved.
- [ ] Results can be regenerated.

---

## 7. Success Criteria

The project should eventually demonstrate the following capabilities.

| Area | Demonstrable capability |
|---|---|
| Python | Maintainable, tested Python application |
| Data engineering | Reliable ingestion, normalization, and validation |
| Statistics | EDA, statistical analysis, and hypothesis testing |
| Feature engineering | Point-in-time feature generation |
| Classical ML | Regression, classification, and tree-based models |
| Deep learning | PyTorch model development and experimentation |
| Evaluation | Walk-forward validation and error analysis |
| Calibration | Reliable probability estimation |
| Uncertainty | Quantification and interpretation of predictive uncertainty |
| Experimentation | Reproducible experiment tracking |
| ML engineering | Training, artifacts, inference, and CLI workflows |
| Communication | Clear reports, visualizations, and research documentation |

The project is successful as a portfolio when an ML engineer or hiring manager can inspect the repository and independently verify these capabilities.

Predictive profitability is not a required success criterion.

---

## 8. Scope Boundaries

The initial project remains:

- Python-based.
- Local-first.
- CPU-compatible.
- CUDA-capable where practical.
- Modular rather than distributed.
- Research-oriented.
- Independent of mandatory paid APIs.
- Free from automated real-money betting.

Infrastructure should grow only when actual research requirements justify it.

---

## 9. Development Strategy

The recommended implementation order is:

1. Establish the engineering foundation.
2. Research data availability and limitations.
3. Build ingestion and validation.
4. Perform exploratory analysis.
5. Develop features and statistical baselines.
6. Build and compare classical ML models.
7. Establish rigorous evaluation and calibration.
8. Investigate deep learning.
9. Develop market discrepancy research.
10. Consolidate experiment tracking, inference, and reporting.

**Do not skip foundational phases to reach neural networks faster.**

A repository containing a well-evaluated gradient-boosting model, a robust temporal validation pipeline, and reproducible experiments is stronger ML evidence than a collection of impressive neural-network architectures without credible evaluation.

---

## 10. Final Objective

NBA Degenerate Gambler should serve as a public, inspectable demonstration of applied machine learning competence.

It should show not only that models can be trained, but that the developer understands:

- Why a model was selected.
- How its data was obtained.
- Which information was available at prediction time.
- How its features were constructed.
- How its performance was evaluated.
- Whether its probabilities are calibrated.
- Where it fails.
- Whether its results are reproducible.
- Whether its complexity is justified.

**The final product is not just a prediction model. It is an evidence-backed ML research platform.**
