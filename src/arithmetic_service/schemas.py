"""Pydantic schemas for arithmetic service API."""

from pydantic import BaseModel, Field


class CalculationRequest(BaseModel):
    """Request payload containing two numeric operands."""
    a: float = Field(..., description="First numeric operand")
    b: float = Field(..., description="Second numeric operand")


class CalculationResponse(BaseModel):
    """Response payload containing calculation result and metadata."""
    operation: str = Field(..., description="Arithmetic operation name")
    a: float = Field(..., description="First operand")
    b: float = Field(..., description="Second operand")
    result: float = Field(..., description="Calculated result")


class ErrorResponse(BaseModel):
    """Standard error response payload."""
    detail: str = Field(..., description="Description of the error")


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = Field(default="healthy", description="Service health status")
