"""Integration tests for FastAPI arithmetic endpoints."""

import pytest
from fastapi.testclient import TestClient
from arithmetic_service.api import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_add_endpoint_success():
    response = client.post("/add", json={"a": 5.0, "b": 3.0})
    assert response.status_code == 200
    data = response.json()
    assert data["operation"] == "add"
    assert data["a"] == 5.0
    assert data["b"] == 3.0
    assert data["result"] == 8.0


def test_add_endpoint_negative_floats():
    response = client.post("/add", json={"a": -4.5, "b": 2.5})
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == -2.0


def test_subtract_endpoint_success():
    response = client.post("/subtract", json={"a": 10.0, "b": 4.0})
    assert response.status_code == 200
    data = response.json()
    assert data["operation"] == "subtract"
    assert data["result"] == 6.0


def test_subtract_endpoint_negative_result():
    response = client.post("/subtract", json={"a": 3.0, "b": 7.0})
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == -4.0


def test_multiply_endpoint_success():
    response = client.post("/multiply", json={"a": 6.0, "b": 7.0})
    assert response.status_code == 200
    data = response.json()
    assert data["operation"] == "multiply"
    assert data["result"] == 42.0


def test_multiply_endpoint_zero():
    response = client.post("/multiply", json={"a": 9.5, "b": 0.0})
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == 0.0


def test_divide_endpoint_success():
    response = client.post("/divide", json={"a": 20.0, "b": 4.0})
    assert response.status_code == 200
    data = response.json()
    assert data["operation"] == "divide"
    assert data["result"] == 5.0


def test_divide_by_zero_error():
    response = client.post("/divide", json={"a": 10.0, "b": 0.0})
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Division by zero is not allowed"


def test_validation_error_invalid_type():
    response = client.post("/add", json={"a": "invalid", "b": 2.0})
    assert response.status_code == 422


def test_validation_error_missing_field():
    response = client.post("/divide", json={"a": 5.0})
    assert response.status_code == 422
