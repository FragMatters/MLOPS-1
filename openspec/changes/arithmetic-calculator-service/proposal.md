# Proposal

## Why

Provide a robust, automated, and observable microservice for arithmetic operations (addition, subtraction, multiplication, division) adhering to modern MLOps software engineering standards. Implementing this with FastAPI, Pytest, Evidently, and Jenkins using `uv` packaging establishes a clean foundation for automated testing, API exposure, continuous integration, and data quality monitoring.

## What Changes

- Initialize Python project management and dependency resolution using `uv` (`pyproject.toml`).
- Implement arithmetic domain logic covering Addition, Subtraction, Multiplication, and Division (with proper zero-division handling and input validation).
- Expose arithmetic operations via a FastAPI application with structured request/response schemas and OpenAPI documentation.
- Implement comprehensive unit and API integration tests using `pytest` and `httpx` (FastAPI `TestClient`).
- Integrate Evidently to track arithmetic calculation records and generate data quality and data drift summary reports.
- Define a Jenkins declarative pipeline (`Jenkinsfile`) to automate virtual environment setup with `uv`, execute Pytest suites, and generate Evidently monitoring reports.

## Capabilities

### New Capabilities
- `arithmetic-api`: Exposes arithmetic operations (addition, subtraction, multiplication, division) via core functions and FastAPI REST API endpoints with schema validation and error handling.
- `calculation-monitoring`: Provides automated data quality and drift evaluation for arithmetic input/output payloads using the Evidently metrics and reporting framework.

### Modified Capabilities
None.

## Impact

- Adds new project structure managed with `uv` (`pyproject.toml`).
- Adds FastAPI application modules (`src/arithmetic_service/`).
- Adds Pytest test suites (`tests/`).
- Adds Evidently report generation scripts and monitoring pipeline components.
- Adds Jenkins CI pipeline configuration (`Jenkinsfile`).
