# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Python automation project for expense analysis. Focus on data processing, validation, and reporting with emphasis on reliability and maintainability.

## Development Environment

**Setup:**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Common Commands:**
- `pip install -r requirements.txt` — install dependencies
- `python -m pytest` — run all tests
- `python -m pytest tests/test_module.py::test_function` — run single test
- `python -m pytest -v` — verbose test output
- `python script.py` — run automation script

## Code Architecture

- **Root scripts** — entry points for automation tasks (e.g., `main.py`, `process_expenses.py`)
- **`modules/`** — core logic organized by domain (parsing, validation, aggregation, export)
- **`tests/`** — mirror source structure with `test_*.py` files
- **`data/`** — input files, raw data (add to `.gitignore`)
- **`output/`** — generated reports, exports (add to `.gitignore`)
- **`config.py`** or `.env`** — configuration, credentials

## Key Patterns for Automation

**Error Handling & Logging:**
- Use logging module, not print. Configure in `config.py` or at script startup.
- Catch and log errors before exiting. Provide context (file name, row number, invalid value).
- Fail fast on data validation (e.g., invalid headers, missing required columns).

**Data Validation:**
- Validate inputs at boundaries (file read, API response, user input).
- Use schema validation (e.g., `dataclasses`, `pydantic` if needed) for structured data.
- Log validation failures with the problematic data point and expected format.

**Idempotency:**
- Design tasks to be safely re-run without duplication (e.g., check if row already processed before insert).
- Use transaction/rollback patterns for file operations when possible.

**Configuration Management:**
- Externalize paths, thresholds, API endpoints to `config.py` or environment variables.
- Do not hardcode file paths or credentials.

**Testing:**
- Unit tests for pure functions (parsing, calculations, transformations).
- Integration tests for end-to-end flows (file read → process → export).
- Mock external dependencies (APIs, file I/O if possible).

**Dependencies:**
- Keep requirements minimal. Prefer stdlib when reasonable.
- Pin versions in `requirements.txt` for reproducibility.
- Document why a dependency is needed (inline comment in requirements or README).

## Common Tasks

**Adding a new data source:**
1. Create parser function in `modules/parsers.py` (or similar).
2. Add validation in `modules/validation.py`.
3. Write unit tests in `tests/test_parsers.py`.
4. Integrate into main script with error handling.

**Modifying report format:**
1. Update export logic in `modules/export.py` (or similar).
2. Add test case for new format in `tests/test_export.py`.
3. Verify with sample data before committing.

## Git Practices

- Commit message: describe the what and why, not the how.
- One feature/fix per commit when possible.
- Keep commits small and reviewable.
