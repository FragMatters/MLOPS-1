# Arithmetic Calculator Microservice (MLOps Pipeline)

A complete Python arithmetic service implementing **Addition (A)**, **Subtraction (B)**, **Multiplication (C)**, and **Division (D)** integrated with **FastAPI**, **Pytest**, **Evidently AI**, and **Jenkins**, managed using the **`uv`** package manager.

---

## Features

- **Four Core Arithmetic Operations**:
  - **A. Addition**: Computes $a + b$ with support for floats and negative numbers.
  - **B. Subtraction**: Computes $a - b$.
  - **C. Multiplication**: Computes $a \times b$.
  - **D. Division**: Computes $a / b$ with explicit zero-division prevention (HTTP 400).
- **FastAPI REST API**: Automatic OpenAPI/Swagger documentation, strict Pydantic validation (HTTP 422 for non-numeric payloads), and health check endpoint.
- **Evidently AI Monitoring**: Captures calculation transactions and generates visual HTML and summary JSON data quality and drift reports.
- **Automated Testing with Pytest**: Comprehensive unit and API integration tests with JUnit XML test reporting.
- **Jenkins CI/CD**: Declarative `Jenkinsfile` for automated build, test execution, Evidently report generation, and artifact archiving.
- **Package Management via `uv`**: Ultra-fast environment resolution and dependency management.
- **Editor Friendly**: Compatible with VSCode, Notepad++, or any standard text editor.

---

## Project Structure

```text
MLOPS-1/
├── Jenkinsfile                  # Jenkins Declarative CI/CD Pipeline
├── pyproject.toml               # Project dependencies and tool configuration (uv)
├── README.md                    # Project documentation
├── src/
│   └── arithmetic_service/
│       ├── __init__.py          # Package initialization & pandas-evidently compatibility
│       ├── core.py              # Pure arithmetic functions (add, subtract, multiply, divide)
│       ├── schemas.py           # Pydantic models for API request/response validation
│       ├── api.py               # FastAPI application with arithmetic endpoints
│       └── monitoring.py        # Evidently transaction logger and report generator
├── tests/
│   ├── __init__.py
│   ├── test_core.py             # Unit tests for core arithmetic operations
│   ├── test_api.py              # Integration tests for FastAPI endpoints
│   └── test_monitoring.py       # Tests for Evidently data logging and generation
├── reports/                     # Output directory for test results and Evidently reports
│   ├── junit-results.xml        # JUnit test result artifact
│   ├── data_quality_report.html # Visual interactive Evidently HTML report
│   ├── data_quality_report.json # Machine-readable Evidently metrics summary
│   └── transactions.jsonl       # Logged calculation transactions
└── openspec/                    # OpenSpec change management artifacts
```

---

## Getting Started

### 1. Prerequisites
- Python 3.10+
- `uv` package manager (`curl -LsSf https://astral.sh/uv/install.sh | sh`)

### 2. Environment Setup
Synchronize dependencies and initialize the virtual environment:
```bash
uv sync
```

### 3. Running Unit and API Tests with Pytest
Execute the full test suite with verbose output and JUnit reporting:
```bash
uv run pytest --junitxml=reports/junit-results.xml -v
```

### 4. Running the FastAPI Service
Start the live Uvicorn ASGI server:
```bash
uv run uvicorn arithmetic_service.api:app --reload --host 0.0.0.0 --port 8000
```
- Interactive API Documentation (Swagger UI): `http://127.0.0.1:8000/docs`
- Alternative Documentation (ReDoc): `http://127.0.0.1:8000/redoc`
- Health check: `http://127.0.0.1:8000/health`

#### Example API Requests via curl:

**A. Addition:**
```bash
curl -X POST http://127.0.0.1:8000/add \
  -H "Content-Type: application/json" \
  -d '{"a": 15.5, "b": 4.5}'
# Response: {"operation":"add","a":15.5,"b":4.5,"result":20.0}
```

**B. Subtraction:**
```bash
curl -X POST http://127.0.0.1:8000/subtract \
  -H "Content-Type: application/json" \
  -d '{"a": 25.0, "b": 7.0}'
# Response: {"operation":"subtract","a":25.0,"b":7.0,"result":18.0}
```

**C. Multiplication:**
```bash
curl -X POST http://127.0.0.1:8000/multiply \
  -H "Content-Type: application/json" \
  -d '{"a": 6.0, "b": 7.0}'
# Response: {"operation":"multiply","a":6.0,"b":7.0,"result":42.0}
```

**D. Division:**
```bash
curl -X POST http://127.0.0.1:8000/divide \
  -H "Content-Type: application/json" \
  -d '{"a": 50.0, "b": 5.0}'
# Response: {"operation":"divide","a":50.0,"b":5.0,"result":10.0}
```

**Division by Zero Handling:**
```bash
curl -X POST http://127.0.0.1:8000/divide \
  -H "Content-Type: application/json" \
  -d '{"a": 10.0, "b": 0.0}'
# Response: HTTP 400 {"detail":"Division by zero is not allowed"}
```

---

## Evidently AI Monitoring

To evaluate transaction data quality, detect distribution drift, and generate reports:
```bash
uv run python -m arithmetic_service.monitoring
```
Generated artifacts in `reports/`:
- `data_quality_report.html`: Visual report openable in any browser.
- `data_quality_report.json`: JSON summary for automated ingestion.
- `transactions.jsonl`: Log of arithmetic computations.

---

## Jenkins CI/CD Pipeline

The project includes a declarative `Jenkinsfile` with the following stages:
1. **Checkout**: Retrieves source code.
2. **Setup Environment & Dependencies**: Auto-installs `uv` if missing and runs `uv sync`.
3. **Run Unit & API Tests**: Runs `pytest` and emits `reports/junit-results.xml`.
4. **Generate Evidently Monitoring Reports**: Executes the Evidently monitoring script.
5. **Post Actions**: Publishes JUnit test results and archives `reports/**` artifacts (HTML and JSON).

---

## Editor Support (VSCode / Notepad++)
- **VSCode**: Open this folder in VSCode (`code .`). The `.venv` environment will be detected automatically by the Python extension.
- **Notepad++**: Source files in `src/arithmetic_service/`, test files in `tests/`, and the `Jenkinsfile` can be viewed and edited in Notepad++.
