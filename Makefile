.DEFAULT_GOAL := help

UV ?= uv

.PHONY: help
.PHONY: format format-check lint test
.PHONY: diff-check check-fast ci-fast

# --------------------------------------------------
# Help
# --------------------------------------------------

help: ## Show available commands
	@grep -E '^[a-zA-Z0-9_-]+:.*?## ' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  %-16s %s\n", $$1, $$2}'

# --------------------------------------------------
# Formatting
# --------------------------------------------------

format: ## Format Python source files
	$(UV) run ruff format .

format-check: ## Check Python formatting without modifying files
	$(UV) run ruff format --check .

# --------------------------------------------------
# Linting
# --------------------------------------------------

lint: ## Run Ruff lint checks
	$(UV) run ruff check .

# --------------------------------------------------
# Testing
# --------------------------------------------------

test: ## Run the test suite
	$(UV) run pytest

# --------------------------------------------------
# General checks
# --------------------------------------------------

diff-check: ## Check Git diff for whitespace errors
	git diff --check
	git diff --cached --check

check-fast: diff-check ## Run fast documentation and diff checks

ci-fast: format-check lint test diff-check ## Run the fast CI quality gate

