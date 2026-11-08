# AGENTS.md

# NBA-DEGENERATE-GAMBLER — Agent Instructions

## 1. Project Identity

NBA-DEGENERATE-GAMBLER is a local-first, research-oriented NBA forecasting platform.

Its primary objectives are:

1. Forecast NBA game outcomes and scores.
2. Forecast individual player performances.
3. Compare model predictions against sportsbook-implied probabilities.
4. Investigate potential statistical discrepancies through rigorous historical evaluation.

The project is built with Python and PyTorch.

### Core Principles

- Research before implementation.
- Data quality before model complexity.
- Statistical baselines before deep learning.
- Reproducibility over convenience.
- Temporal correctness over inflated metrics.
- Evidence over assumptions.
- Local execution over unnecessary infrastructure.

The system is intended for forecasting research and paper-trading simulations. Real-money betting execution is outside project scope.

---

## 2. Instructions for Coding Agents

You are an engineering and research agent working on NBA-DEGENERATE-GAMBLER.

You must understand the existing codebase before changing it.

### 2.1 Before Starting Work

1. Read this file completely.
2. Read `PRD.md`.
3. Read `FEATURE-LIST.md` when available.
4. Read `ARCHITECTURE.md` when available.
5. Inspect the relevant source code and tests.
6. Inspect the current Git branch and working tree.
7. Identify existing conventions before introducing new ones.
8. Check whether the requested functionality already exists.

Do not assume that documentation perfectly describes the implementation.

When documentation and implementation disagree:

- Inspect the relevant code.
- Determine which behavior is intentional.
- Identify the discrepancy.
- Avoid silently changing established behavior.
- Update the relevant documentation when the implementation changes.

### 2.2 Scope Discipline

- Implement only what the task requires.
- Avoid unrelated refactoring.
- Do not introduce speculative abstractions.
- Do not add dependencies without justification.
- Do not create infrastructure without a concrete requirement.
- Do not silently change public interfaces.
- Do not remove existing functionality without authorization.
- Do not claim that unimplemented functionality exists.

Prefer small, reviewable changes.

### 2.3 Research Discipline

When implementing statistical or machine learning functionality:

1. Identify the mathematical or statistical objective.
2. Inspect existing implementations and dependencies.
3. Verify formulas and assumptions.
4. Identify possible sources of bias or leakage.
5. Implement the simplest defensible approach.
6. Write tests for normal and edge cases.
7. Document important assumptions.

Do not invent mathematical behavior to make an implementation appear complete.

When external research is necessary, prefer primary documentation, academic publications, official data documentation, and reproducible technical references.

Record important research findings and source limitations in the appropriate documentation.

### 2.4 Uncertainty and Missing Information

When a requirement is ambiguous:

- Inspect existing project decisions.
- Prefer consistency with the established architecture.
- Choose conservative defaults when the impact is small.
- Ask for clarification when an assumption could materially change architecture, data semantics, or research validity.

Never fabricate data coverage, historical availability, benchmark results, or model performance.

---

## 3. Architecture and Engineering Rules

### 3.1 Architectural Style

NBA-DEGENERATE-GAMBLER uses a modular monolithic architecture.

Keep responsibilities separated across:

- Ingestion.
- Data normalization.
- Data validation.
- Storage.
- Feature engineering.
- Statistical baselines.
- Model implementations.
- Training.
- Evaluation.
- Calibration.
- Uncertainty estimation.
- Market analysis.
- Inference.
- Experiment tracking.
- Reporting.
- CLI.

Avoid unnecessary distributed systems and service boundaries.

The initial architecture is local-first.

### 3.2 Python Standards

- Target Python 3.12 or newer.
- Use `uv` for dependency and environment management.
- Use type hints for public interfaces.
- Prefer explicit interfaces over implicit behavior.
- Keep functions focused and reasonably small.
- Use meaningful names.
- Avoid unnecessary global state.
- Use structured exceptions where appropriate.
- Avoid swallowing exceptions.
- Avoid broad `except Exception` unless the boundary genuinely requires it.
- Keep configuration separate from implementation.
- Use Pydantic for appropriate validation boundaries.
- Follow the project's configured formatter and linter.

Do not introduce multiple libraries that solve the same problem without a clear reason.

### 3.3 Dependencies

Before adding a dependency:

1. Determine whether an existing dependency already solves the problem.
2. Check compatibility with the project's Python version.
3. Consider installation size and transitive dependencies.
4. Consider CPU and GPU compatibility.
5. Check maintenance status and licensing.
6. Explain why the dependency is necessary.

Use the existing package manager and lockfile.

Never manually modify generated lockfile content.

### 3.4 Data Processing

Prefer:

- Polars for efficient data processing.
- Pandas where ecosystem compatibility requires it.
- NumPy for numerical operations.
- DuckDB for analytical queries.
- Parquet for columnar storage.

Avoid unnecessary conversions between data representations.

Do not load entire historical datasets into memory when processing can be streamed, partitioned, or batched.

### 3.5 Local Hardware

The initial development environment targets:

- NVIDIA GTX 1650.
- 16 GB system RAM.
- Linux.
- CPU fallback.

Keep model architectures and training configurations compatible with limited hardware.

Avoid:

- Unnecessarily large Transformers.
- Excessive sequence lengths.
- Unbounded batch sizes.
- Unnecessary GPU memory allocation.
- Mandatory cloud execution.
- Distributed training requirements.

CUDA support is optional. CPU execution must remain supported.

---

## 4. Data Integrity and Temporal Correctness

Data integrity is a foundational requirement, not an optional improvement.

### 4.1 Data Provenance

Every ingested dataset must retain sufficient metadata to identify:

- Source.
- Retrieval timestamp.
- Historical coverage.
- Schema or format version.
- Known limitations.
- Licensing restrictions where relevant.

Preserve raw source data whenever practical.

Never silently overwrite raw historical snapshots.

### 4.2 Temporal Fields

The system distinguishes:

| Field | Meaning |
|---|---|
| `event_time` | When the real-world event occurred |
| `available_at` | When the information became available |
| `prediction_timestamp` | When the forecast was generated |

Do not treat these timestamps as interchangeable.

### 4.3 Look-Ahead Bias

Historical predictions must use only information available at the prediction timestamp.

Forbidden examples:

- Using final game statistics to predict that same game.
- Using future player availability information.
- Using future roster information.
- Using odds published after the simulated decision time.
- Using statistics updated after the prediction timestamp.
- Calculating rolling features that include the target game.

All historical features must respect point-in-time availability.

### 4.4 Historical Identity

Player and team associations must be historically accurate.

Do not assume:

- Current team equals historical team.
- Current roster equals historical roster.
- Current player role equals historical player role.
- Current player availability reflects historical availability.

### 4.5 Missing Data

Never silently replace missing data with fabricated values.

Every imputation strategy must be:

- Explicit.
- Documented.
- Appropriate for the feature.
- Applied consistently between training and inference.

Preserve missingness information when it carries analytical value.

### 4.6 External Data Sources

External APIs and datasets are unreliable dependencies.

Agents must:

- Handle rate limits.
- Implement appropriate retries.
- Use timeouts.
- Validate responses.
- Detect incomplete downloads.
- Avoid unnecessary repeated requests.
- Preserve source errors and relevant diagnostics.

Do not assume unofficial NBA endpoints will remain stable.

Data-source adapters must remain replaceable.

---

## 5. Machine Learning and Statistical Research Rules

### 5.1 Baseline-First Development

Before implementing a sophisticated model, identify the appropriate baseline.

Expected baseline progression:

1. Historical home-court baseline.
2. Elo.
3. Logistic regression.
4. Linear regression.
5. XGBoost.
6. LightGBM.
7. PyTorch models.

A complex model must justify its additional complexity through out-of-sample evidence.

### 5.2 Evaluation

Primary evaluation must be chronological.

Do not randomly split individual games across training, validation, and testing for primary performance claims.

Use:

- Chronological train/validation/test splits.
- Expanding-window evaluation.
- Rolling-window evaluation.
- Walk-forward backtesting.

Calibration must be fitted on validation data, not the final test set.

### 5.3 Probability Quality

Accuracy alone is insufficient for probabilistic forecasting.

Where applicable, report:

- Log Loss.
- Brier Score.
- ROC-AUC.
- Expected Calibration Error.
- Reliability diagrams.
- Prediction interval coverage.

Do not describe an uncalibrated model as reliable merely because it predicts many winners correctly.

### 5.4 Regression Quality

Where applicable, report:

- MAE.
- RMSE.
- R².
- Prediction interval coverage.
- Residual distributions.

Evaluate player-level predictions separately from game-level predictions.

### 5.5 Uncertainty

Predictions should distinguish point estimates from uncertainty.

Where appropriate, use:

- Predictive distributions.
- Prediction intervals.
- Ensemble variance.
- Monte Carlo dropout.
- Calibration methods.

Never present a probabilistic forecast as a guaranteed outcome.

### 5.6 Market Research

Market analysis is logically separate from the forecasting model.

Agents must distinguish:

- Raw implied probability.
- No-vig implied probability.
- Model probability.
- Model-market difference.
- Expected value.
- Realized return.
- Closing-line value.

Market evaluation must account for:

- Odds timestamps.
- Bookmaker identity.
- Vig.
- Execution assumptions.
- Sample size.
- Statistical uncertainty.
- Data availability.

Historical closing odds cannot be treated as prices available at arbitrary earlier times.

Do not claim profitability from:

- Small samples.
- In-sample performance.
- Untested assumptions.
- Backtests with future information.
- Results that ignore bookmaker margins.

All market strategies remain research and paper-trading simulations.

### 5.7 Reproducibility

Every meaningful experiment must record:

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

Preserve negative results.

Do not delete failed experiments merely because their results are inconvenient.

---

## 6. Testing Requirements

Tests are part of implementation, not a cleanup task for later.

### 6.1 Unit Tests

Test:

- Mathematical functions.
- Statistical transformations.
- Feature calculations.
- Data normalization.
- Probability conversions.
- Odds calculations.
- Validation logic.
- Model output shapes.
- Edge cases.

### 6.2 Integration Tests

Test:

- Ingestion adapters.
- Data storage.
- Feature pipelines.
- Training workflows.
- Evaluation workflows.
- Inference.
- Experiment tracking.

Use fixtures and controlled test datasets where appropriate.

Tests must not depend on unreliable external APIs unless explicitly designed as integration tests.

### 6.3 Research Tests

Test:

- Chronological split behavior.
- Temporal feature boundaries.
- Prediction timestamp consistency.
- Leakage prevention.
- Calibration data separation.
- Historical player-team associations.
- Odds timestamp correctness.

### 6.4 Test Quality

- Do not write tests that merely duplicate implementation details.
- Test observable behavior.
- Include boundary conditions.
- Include missing-data cases.
- Include invalid-input cases.
- Keep tests deterministic where practical.
- Avoid unnecessary network access.

A model that trains successfully but violates temporal correctness is considered broken.

---

## 7. Documentation Requirements

Documentation must describe actual system behavior.

Important documents:

| Document | Responsibility |
|---|---|
| `README.md` | Project overview and getting started |
| `PRD.md` | Product requirements |
| `FEATURE-LIST.md` | Implementation tasks and acceptance criteria |
| `ARCHITECTURE.md` | Technical architecture |
| `AGENTS.md` | Coding agent rules |
| `docs/methodology/` | Statistical and research methodology |
| `docs/datasets/` | Data sources, coverage, and limitations |
| `docs/decisions/` | Architectural Decision Records |

When a change affects architecture, update `ARCHITECTURE.md`.

When a change affects research methodology, update the relevant methodology documentation.

When a change affects user-facing behavior, update `README.md` or the appropriate usage documentation.

Do not document hypothetical functionality as implemented functionality.

---

## 8. Git Workflow

### Branching Model

```text
feat/short-description ──┐
fix/short-description ───┤
refactor/short-desc ─────┼──> develop ──> main
test/short-description ──┤
docs/short-description ──┤
chore/short-description ─┤
ci/short-description ────┤
perf/short-description ──┤
build/short-description ─┘
```

All merges use `--no-ff`. No fast-forward merges.

### Branch Naming

```text
feat/add-player-features
fix/handle-missing-game-data
refactor/simplify-feature-pipeline
test/add-elo-edge-cases
docs/update-architecture
chore/update-dependencies
ci/add-test-workflow
perf/optimize-parquet-loading
build/configure-python-package
```

Rules:

- Lowercase.
- Hyphens as separators.
- Short and descriptive.
- Use the appropriate branch prefix.

### Commit Format

```text
type(scope): commit message
```

#### Allowed Types

| Type | Use |
|---|---|
| `feat` | New feature |
| `fix` | Bug fix |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `test` | Adding or correcting tests |
| `docs` | Documentation only |
| `chore` | Build process, dependencies, tooling |
| `ci` | CI/CD configuration |
| `perf` | Performance improvement |
| `build` | Build system or external dependency changes |

#### Allowed Scopes

Scopes should match a project module or major responsibility.

| Scope | Responsibility |
|---|---|
| `ingestion` | Data ingestion and source adapters |
| `data` | Data schemas, normalization, validation, storage |
| `features` | Feature engineering |
| `baselines` | Statistical baseline models |
| `game` | Game forecasting |
| `player` | Player forecasting |
| `models` | Shared model components and architectures |
| `training` | Model training |
| `evaluation` | Evaluation and backtesting |
| `calibration` | Probability calibration |
| `uncertainty` | Prediction uncertainty |
| `market` | Sportsbook odds and market analysis |
| `experiments` | Experiment tracking and reproducibility |
| `inference` | Prediction execution |
| `reporting` | Reports and visualizations |
| `cli` | Command-line interface |
| `config` | Configuration |
| `testing` | Test infrastructure |
| `docs` | Documentation |
| `workflow` | CI/CD and automation |
| `workspace` | Packaging and project configuration |

A commit without a scope is permitted only for genuinely project-wide changes, such as dependency updates.

#### Examples

```text
feat(features): add rolling team efficiency metrics
fix(ingestion): handle incomplete nba api responses
refactor(data): simplify player normalization
test(baselines): add elo edge cases
docs(architecture): document feature pipeline
chore(config): update dependency constraints
ci(workflow): add python test workflow
perf(data): optimize parquet loading
build(workspace): configure package entry points
```

### Merge Rules

#### Feature → develop

1. Develop on an appropriate feature branch.
2. Keep commits focused and meaningful.
3. Squash the branch's work into one commit before merging.
4. Update `TODO.md` in the same squash commit when the completed work corresponds to an existing task.
5. Merge into `develop` using `--no-ff`.
6. Run the appropriate quality gate after the merge.

`TODO.md` conventions:

- Keep it as a single flat list.
- One task per `- [ ]` line.
- `- [~]` marks an in-progress task.
- Completed tasks are deleted, not converted into `- [x]`.
- Never create a separate follow-up commit directly on `develop` merely to update a completed task.
- Keep the board concise and actionable.
- A task should represent a meaningful unit of work.

#### Merge Quality Gates

**Code-carrying branch**

Before merging:

```bash
uv run ruff format --check .
uv run ruff check .
uv run pytest
```

After merging:

```bash
make ci-fast
```

`make ci-fast` must run the project's fast CI checks, including the configured formatting, linting, type-checking, and test gates.

**Documentation-only branch**

No Python test suite is required when no executable code or configuration changes.

Run:

```bash
git diff --check
make check-fast
```

`make check-fast` must validate documentation and other non-code quality checks.

If these Makefile targets do not exist yet, implement them as part of the project's tooling setup before relying on them. Never pretend a missing gate passed.

#### develop → main

The default landing branch is `develop`.

Merges from `develop` into `main` are user-triggered. Only perform them when the user explicitly requests a release or asks to merge into `main`.

**Code-carrying release gate**

Run:

```bash
uv run ruff format --check .
uv run ruff check .
uv run pytest
make ci-fast
```

**Documentation-only release gate**

Run:

```bash
git diff --check
make check-fast
```

Then:

1. Review the complete diff.
2. Merge `develop` into `main` using `--no-ff`.
3. Verify the resulting merge commit.
4. Do not create a version tag.

**Tag policy**

No Git tags of any kind are permitted in this repository.

Releases must be identified by commit SHA. Version information may be recorded in release documentation or project metadata, but must not be represented by Git tags.

### Forbidden

- Fast-forward merges.
- Direct commits to `main`.
- Direct commits to `develop`.
- Direct TODO completion commits on `develop`.
- Merge commits without a scope in their commit message.
- Git tags of any kind.
- Force-pushing shared branches without explicit authorization.
- Rewriting published branch history without explicit authorization.
- Committing generated datasets or model checkpoints.
- Committing credentials, API keys, or personal tokens.

---

## 9. Data and Artifact Management

### 9.1 Git

Git should track:

- Source code.
- Tests.
- Configuration templates.
- Documentation.
- Small deterministic fixtures.
- Project metadata.
- Reproducible scripts.

Git should not track:

- Large historical datasets.
- Downloaded raw data.
- Generated feature datasets.
- Model checkpoints.
- Large experiment outputs.
- Local caches.
- Credentials.
- Temporary files.

### 9.2 Local Artifacts

Use the established local directory structure:

```text
data/raw/
data/processed/
data/features/
data/metadata/

models/checkpoints/
models/artifacts/

experiments/results/
reports/
```

Do not introduce another artifact directory without a concrete reason.

### 9.3 Configuration and Secrets

- Commit safe configuration templates.
- Keep local credentials outside version control.
- Use environment variables or an appropriate local secret mechanism.
- Never print credentials in logs.
- Never include tokens in exception messages or reports.

---

## 10. CLI and User Experience

The CLI should remain predictable and consistent.

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

Rules:

- Provide useful `--help` output.
- Validate arguments.
- Report failures clearly.
- Avoid unnecessary interactive prompts.
- Support reproducible configuration-driven execution.
- Keep output readable in a terminal.
- Use meaningful exit codes.

Long-running operations should provide useful progress information without overwhelming the terminal.

---

## 11. Agent Execution Protocol

For each task:

### Step 1: Understand

- Read relevant documentation.
- Inspect relevant implementation.
- Identify dependencies.
- Identify constraints.
- Confirm the current Git state.

### Step 2: Plan

Create a concise implementation plan.

Identify:

- Files to modify.
- New files required.
- Relevant tests.
- Potential data or temporal risks.
- Documentation changes.

For small changes, a short plan is sufficient.

For architectural changes, investigate before implementation.

### Step 3: Implement

- Follow existing conventions.
- Keep changes focused.
- Avoid unnecessary dependencies.
- Add tests alongside implementation.
- Preserve backward compatibility where required.

### Step 4: Verify

Run the relevant tests and quality checks.

Do not claim that a command passed unless it was actually executed successfully.

Report:

- Commands executed.
- Checks passed.
- Checks failed.
- Checks not executed.
- Known limitations.

### Step 5: Review

Inspect the final diff.

Check for:

- Unrelated changes.
- Accidental file deletion.
- Debug statements.
- Hardcoded paths.
- Secrets.
- Data leakage.
- Missing tests.
- Inaccurate documentation.
- Generated artifacts accidentally included.

### Step 6: Report

Provide a concise summary:

1. What changed.
2. Why it changed.
3. Important implementation decisions.
4. Tests and checks performed.
5. Remaining limitations.
6. Git branch and commit information, when applicable.

Never claim that work is complete when required tests or validation remain outstanding.

---

## 12. Explicitly Forbidden Agent Behavior

Agents must never:

- Invent historical data.
- Fabricate experiment results.
- Fabricate data-source coverage.
- Hide failed tests.
- Suppress warnings merely to obtain a green test run.
- Introduce future information into historical predictions.
- Use random splits for primary time-dependent evaluation.
- Claim profitability without defensible evidence.
- Change research assumptions silently.
- Add unnecessary infrastructure.
- Introduce dependencies without justification.
- Commit large generated artifacts.
- Commit secrets.
- Modify protected branches directly.
- Create Git tags.
- Delete unrelated files.
- Rewrite project history without authorization.

When something cannot be verified, state that it cannot be verified.

---

## 13. Priority Hierarchy

When instructions or implementation decisions conflict, use this priority order:

1. Explicit user instructions for the current task.
2. This `AGENTS.md`.
3. `PRD.md`.
4. `ARCHITECTURE.md`.
5. `FEATURE-LIST.md`.
6. Relevant architectural decisions.
7. Existing implementation conventions.
8. Agent preferences.

Do not use personal coding preferences to override established project requirements.

If two project documents conflict, identify the conflict instead of silently choosing whichever is more convenient.

---

## 14. Final Engineering Standard

NBA-DEGENERATE-GAMBLER is a research project.

A successful implementation is not merely code that executes.

It must be:

- Statistically defensible.
- Temporally correct.
- Reproducible.
- Tested.
- Maintainable.
- Appropriately scoped.
- Honest about uncertainty and limitations.

The objective is not to build the most complicated NBA prediction model.

The objective is to build a system capable of determining, with evidence, whether a forecasting method actually works.

**Build the evidence first. Optimize the models second.**
