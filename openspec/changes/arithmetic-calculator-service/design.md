# Design

## Context

The repository is a greenfield project establishing an automated, tested, and observable arithmetic microservice. The service implements four core arithmetic operations (addition, subtraction, multiplication, and division) and integrates them with FastAPI for API serving, Pytest for automated unit and contract tests, Evidently AI for transaction data quality and drift monitoring, Jenkins for CI/CD automation, and `uv` for modern Python package and environment management.

See `proposal.md` for overall motivation and `specs/` for behavioral requirements.

## Goals / Non-Goals

**Goals:**
- Provide a clean, modular Python architecture separating core arithmetic business logic from HTTP transport and MLOps monitoring.
- Manage dependencies, virtual environments, and CLI execution cleanly with `uv` (`pyproject.toml`).
- Expose RESTful endpoints via FastAPI with Pydantic request/response validation, automatic OpenAPI docs, and structured error handling (specifically HTTP 400 for division by zero and HTTP 422 for malformed payloads).
- Achieve high Pytest test coverage across all arithmetic operations, API endpoints, and edge cases.
- Integrate Evidently to capture calculation records and generate HTML and JSON reports on data quality and statistical drift.
- Deliver a production-ready declarative `Jenkinsfile` for continuous integration (installing dependencies, running tests, generating reports, archiving artifacts).

**Non-Goals:**
- User authentication, authorization, or role-based access control.
- Distributed database persistence; transaction logging will use structured local files (JSON/CSV) sufficient for Evidently monitoring pipelines.
- Multi-container cluster orchestration (e.g. Kubernetes).

## Decisions

### 1. Package and Environment Management: `uv`
- **Choice**: Use `uv` with a `pyproject.toml` specification.
- **Rationale**: `uv` provides extremely fast dependency resolution, deterministic lockfiles (`uv.lock`), and simple command execution (`uv run pytest`, `uv run uvicorn`).
- **Alternative considered**: Traditional `pip` and `requirements.txt` or `poetry`. `uv` is explicitly requested and provides superior speed and single-tool standardization.

### 2. Architecture and Layout
- **Choice**: Standard `src/` layout:
  ```text
  ├── pyproject.toml
  ├── Jenkinsfile
  ├── README.md
  ├── src/
  │   └── arithmetic_service/
  │       ├── __init__.py
  │       ├── core.py         # Pure arithmetic functions (add, subtract, multiply, divide)
  │       ├── schemas.py      # Pydantic models for requests and responses
  │       ├── api.py          # FastAPI application routes
  │       └── monitoring.py   # Evidently report generator and data logger
  ├── tests/
  │   ├── __init__.py
  │   ├── test_core.py        # Pytest unit tests for core arithmetic
  │   └── test_api.py         # Pytest API integration tests (TestClient)
  └── reports/                # Target directory for Evidently HTML/JSON reports
  ```
- **Rationale**: Strict separation of concerns allows testing pure arithmetic logic independently of FastAPI HTTP layer, and allows standalone invocation of monitoring scripts.

### 3. API Design & Error Handling
- **Endpoints**:
  - `POST /add` -> `{ "a": float, "b": float }` -> `{ "operation": "add", "a": float, "b": float, "result": float }`
  - `POST /subtract` -> `{ "a": float, "b": float }` -> `{ "operation": "subtract", "a": float, "b": float, "result": float }`
  - `POST /multiply` -> `{ "a": float, "b": float }` -> `{ "operation": "multiply", "a": float, "b": float, "result": float }`
  - `POST /divide` -> `{ "a": float, "b": float }` -> `{ "operation": "divide", "a": float, "b": float, "result": float }`
  - `GET /health` -> `{ "status": "healthy" }`
- **Zero Division**: When `b == 0` on `/divide`, return HTTP 400 Bad Request with `{ "detail": "Division by zero is not allowed" }`.
- **Validation**: Pydantic validates numeric inputs, returning HTTP 422 if strings or null values are supplied.

### 4. MLOps Monitoring with Evidently
- **Choice**: Implement an evaluation module using Evidently's `Report` with `DataQualityPreset` and `DataDriftPreset`.
- **Rationale**: Captures operand distributions ($a$, $b$, operation type, results) and compares current transaction batches against a reference distribution to detect anomalous inputs or data shifts.
- **Output**: Generates `reports/data_quality_report.html` and `reports/data_quality_report.json`.

### 5. Jenkins CI/CD Pipeline
- **Choice**: Declarative pipeline (`Jenkinsfile`) with stages:
  1. `Checkout`
  2. `Setup Environment` (install/verify `uv` and run `uv sync`)
  3. `Run Unit & API Tests` (`uv run pytest --junitxml=test-reports.xml`)
  4. `Run Evidently Monitoring` (`uv run python -m arithmetic_service.monitoring`)
  5. `Archive Artifacts` (test results, Evidently HTML/JSON reports)
- **Rationale**: Enables reproducible automated builds in Jenkins.

## Risks / Trade-offs

- **[Evidently dependencies weight]** → Evidently brings dependencies like pandas and pydantic. Mitigation: Pin compatible versions in `pyproject.toml` managed by `uv`.
- **[Floating point precision]** → Standard IEEE 754 float representation in Python may produce minor precision artifacts (e.g., `0.1 + 0.2`). Mitigation: Pytest tests will use `pytest.approx()` for floating-point comparisons.
- **[Jenkins agent tooling availability]** → Build agents may not have `uv` pre-installed. Mitigation: Include a fallback in the Jenkinsfile stage to fetch `uv` standalone binary if absent.
