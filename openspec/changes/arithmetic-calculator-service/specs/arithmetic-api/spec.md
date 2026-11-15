# Spec Delta

## Purpose

Provides core arithmetic calculations (addition, subtraction, multiplication, and division) and exposes them as RESTful API endpoints with schema validation and error responses.

## ADDED Requirements

### Requirement: Addition Calculation
The system SHALL compute the arithmetic sum of two numeric inputs and return the calculated result.

#### Scenario: Successful addition of positive numbers
- **WHEN** two numbers 5 and 3 are submitted for addition
- **THEN** the system returns a result of 8 with status 200

#### Scenario: Addition with negative and floating-point values
- **WHEN** numbers -4.5 and 2.5 are submitted for addition
- **THEN** the system returns a result of -2.0 with status 200

### Requirement: Subtraction Calculation
The system SHALL compute the arithmetic difference by subtracting the second numeric input from the first numeric input and return the calculated result.

#### Scenario: Successful subtraction
- **WHEN** numbers 10 and 4 are submitted for subtraction
- **THEN** the system returns a result of 6 with status 200

#### Scenario: Subtraction resulting in a negative number
- **WHEN** numbers 3 and 7 are submitted for subtraction
- **THEN** the system returns a result of -4 with status 200

### Requirement: Multiplication Calculation
The system SHALL compute the arithmetic product of two numeric inputs and return the calculated result.

#### Scenario: Successful multiplication
- **WHEN** numbers 6 and 7 are submitted for multiplication
- **THEN** the system returns a result of 42 with status 200

#### Scenario: Multiplication by zero
- **WHEN** numbers 9.5 and 0 are submitted for multiplication
- **THEN** the system returns a result of 0.0 with status 200

### Requirement: Division Calculation
The system SHALL compute the quotient of dividing the first numeric input by the second numeric input when the denominator is non-zero.

#### Scenario: Successful division
- **WHEN** numbers 20 and 4 are submitted for division
- **THEN** the system returns a result of 5.0 with status 200

#### Scenario: Division by zero handling
- **WHEN** numbers 10 and 0 are submitted for division
- **THEN** the system rejects the operation with an error message indicating division by zero is not permitted and returns an appropriate client error status

### Requirement: API Input Validation
The system SHALL validate that input payloads contain valid numeric values for the required operands before performing any arithmetic operation.

#### Scenario: Invalid non-numeric input payload
- **WHEN** non-numeric values are supplied for calculation operands
- **THEN** the API returns an HTTP 422 Unprocessable Entity response detailing the validation failure
