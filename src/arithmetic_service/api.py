"""FastAPI application exposing arithmetic calculation endpoints."""

from fastapi import FastAPI, HTTPException, status
from arithmetic_service import core
from arithmetic_service.monitoring import log_transaction
from arithmetic_service.schemas import (
    CalculationRequest,
    CalculationResponse,
    ErrorResponse,
    HealthResponse,
)

app = FastAPI(
    title="Arithmetic Microservice",
    description="FastAPI service for Addition, Subtraction, Multiplication, and Division with Pytest and Evidently monitoring.",
    version="0.1.0",
)


@app.get("/health", response_model=HealthResponse, tags=["Health"])
def health_check() -> HealthResponse:
    """Return health status of the service."""
    return HealthResponse(status="healthy")


@app.post(
    "/add",
    response_model=CalculationResponse,
    status_code=status.HTTP_200_OK,
    tags=["Arithmetic"],
)
def add_endpoint(payload: CalculationRequest) -> CalculationResponse:
    """Add two numbers and return the result."""
    result = core.add(payload.a, payload.b)
    log_transaction("add", payload.a, payload.b, float(result))
    return CalculationResponse(
        operation="add",
        a=payload.a,
        b=payload.b,
        result=float(result),
    )


@app.post(
    "/subtract",
    response_model=CalculationResponse,
    status_code=status.HTTP_200_OK,
    tags=["Arithmetic"],
)
def subtract_endpoint(payload: CalculationRequest) -> CalculationResponse:
    """Subtract operand b from operand a and return the result."""
    result = core.subtract(payload.a, payload.b)
    log_transaction("subtract", payload.a, payload.b, float(result))
    return CalculationResponse(
        operation="subtract",
        a=payload.a,
        b=payload.b,
        result=float(result),
    )


@app.post(
    "/multiply",
    response_model=CalculationResponse,
    status_code=status.HTTP_200_OK,
    tags=["Arithmetic"],
)
def multiply_endpoint(payload: CalculationRequest) -> CalculationResponse:
    """Multiply two numbers and return the result."""
    result = core.multiply(payload.a, payload.b)
    log_transaction("multiply", payload.a, payload.b, float(result))
    return CalculationResponse(
        operation="multiply",
        a=payload.a,
        b=payload.b,
        result=float(result),
    )


@app.post(
    "/divide",
    response_model=CalculationResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse, "description": "Division by zero error"},
    },
    tags=["Arithmetic"],
)
def divide_endpoint(payload: CalculationRequest) -> CalculationResponse:
    """Divide operand a by operand b and return the result."""
    try:
        result = core.divide(payload.a, payload.b)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    log_transaction("divide", payload.a, payload.b, float(result))
    return CalculationResponse(
        operation="divide",
        a=payload.a,
        b=payload.b,
        result=float(result),
    )
