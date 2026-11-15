# Tasks

## 1. Project Initialization & Packaging with uv

- [x] 1.1 Configure `pyproject.toml` with project metadata and required dependencies (`fastapi`, `uvicorn`, `pydantic`, `pytest`, `httpx`, `evidently`, `pandas`) and verify environment resolution with `uv sync`
- [x] 1.2 Scaffold project directories (`src/arithmetic_service/`, `tests/`, `reports/`) with `__init__.py` files and verify module importability

## 2. Core Arithmetic Operations & Unit Testing

- [x] 2.1 Implement core addition and subtraction functions in `src/arithmetic_service/core.py` and verify calculation accuracy and negative/float edge cases with unit tests in `tests/test_core.py` via `uv run pytest`
- [x] 2.2 Implement core multiplication and division functions (including zero-division error raising) in `src/arithmetic_service/core.py` and verify functionality with unit tests in `tests/test_core.py` via `uv run pytest`

## 3. FastAPI REST Endpoints & API Integration Testing

- [x] 3.1 Define Pydantic request (`CalculationRequest`), response (`CalculationResponse`), and error schemas in `src/arithmetic_service/schemas.py` and verify validation rules
- [x] 3.2 Implement FastAPI application routes (`/add`, `/subtract`, `/multiply`, `/divide`, and `/health`) in `src/arithmetic_service/api.py` and verify successful responses, HTTP 400 division-by-zero handling, and HTTP 422 schema validation failures via integration tests in `tests/test_api.py` using `uv run pytest`

## 4. Evidently Monitoring & Drift Evaluation

- [x] 4.1 Implement calculation payload logging and synthetic baseline reference generation in `src/arithmetic_service/monitoring.py` and verify structured dataset serialization
- [x] 4.2 Implement Evidently evaluation runner generating visual HTML reports (`reports/data_quality_report.html`) and summary JSON metrics (`reports/data_quality_report.json`), and verify execution via `uv run python -m arithmetic_service.monitoring`

## 5. Jenkins CI/CD Pipeline Configuration & Verification

- [x] 5.1 Create declarative `Jenkinsfile` orchestrating dependency installation with `uv`, execution of Pytest test suites, generation of Evidently monitoring reports, and archiving of HTML/XML report artifacts
- [x] 5.2 Run complete local test and monitoring pipeline and verify all Pytest tests pass and report files are populated in `reports/`
