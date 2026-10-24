### PI Testing with FastAPI TestClient  -- Create tests/api/test_employee_api.py

'''
Now we will test the application through HTTP requests.

'''

def test_create_employee_success(client):  # FastAPI provides TestClient for testing an application without starting a separate HTTP server.

    payload = {
        "name": "Arun Kumar",
        "email": "arun@example.com",
        "salary": 50000,
    }

    response = client.post(  
        "/api/employees",
        json=payload,
    )
## This sends a test request to the application.
## It does not require you to run Uvicorn in another terminal.


    assert response.status_code == 201

    body = response.json()  
    # This sends a test request to the application.
    # It does not require you to run Uvicorn in another terminal.

    assert body["employee_id"] > 0
    assert body["name"] == "Arun Kumar"
    assert body["email"] == "arun@example.com"
    assert body["salary"] == 50000



def test_get_employee_success(client, sample_employee):

    response = client.get(
        f"/api/employees/{sample_employee.employee_id}"
    )

    assert response.status_code == 200

    body = response.json()

    assert body["name"] == "Arun Kumar"
    assert body["email"] == "arun@example.com"



def test_get_employee_not_found(client):

    response = client.get("/api/employees/999")

    assert response.status_code == 404

    assert response.json()["detail"] == (
        "Employee 999 was not found."
    )



def test_list_employees(client, sample_employee):

    response = client.get("/api/employees")

    assert response.status_code == 200

    body = response.json()

    assert len(body) == 1

    assert body[0]["name"] == "Arun Kumar"



def test_update_employee(client, sample_employee):

    payload = {
        "name": "Arun Kumar Updated",
        "email": "arun.updated@example.com",
        "salary": 65000,
    }

    response = client.put(
        f"/api/employees/{sample_employee.employee_id}",
        json=payload,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["name"] == "Arun Kumar Updated"
    assert body["email"] == "arun.updated@example.com"
    assert body["salary"] == 65000



def test_delete_employee(client, sample_employee):

    employee_id = sample_employee.employee_id

    response = client.delete(
        f"/api/employees/{employee_id}"
    )

    assert response.status_code == 204  # Verifies that the API returns HTTP 204 No Content.
    assert response.content == b""

### Verifies that the response body is empty. b"" represents an empty bytes object in Python.
### HTTP responses store their raw content as bytes.

#### Why are both assertions necessary?
    # The first verifies that the API returned the correct HTTP status.
    # The second verifies that the API did not return any response content.

    # Note: HTTP 204 No Content responses must not contain a response body.

    get_response = client.get(
        f"/api/employees/{employee_id}"
    )

    assert get_response.status_code == 404



### Positive testing verifies that valid input is accepted.

def test_create_employee_with_valid_data(client):

    response = client.post(
        "/api/employees",
        json={
            "name": "Meena Devi",
            "email": "meena@example.com",
            "salary": 45000,
        },
    )

    assert response.status_code == 201



#### Negative testing --> Negative testing verifies that invalid input or invalid operations are rejected correctly.

def test_create_employee_with_invalid_email(client):

    response = client.post(
        "/api/employees",
        json={
            "name": "Meena Devi",
            "email": "invalid-email",
            "salary": 45000,
        },
    )

    assert response.status_code == 422  #HTTP 422 Unprocessable Entity (or Unprocessable Content)


def test_create_employee_with_negative_salary(client):

    response = client.post(
        "/api/employees",
        json={
            "name": "Meena Devi",
            "email": "meena@example.com",
            "salary": -1000,
        },
    )

    assert response.status_code == 422


def test_create_employee_with_missing_name(client):

    response = client.post(
        "/api/employees",
        json={
            "email": "meena@example.com",
            "salary": 45000,
        },
    )

    assert response.status_code == 422


def test_create_employee_with_duplicate_email(
    client,
    sample_employee,
):

    response = client.post(
        "/api/employees",
        json={
            "name": "Another Arun",
            "email": "arun@example.com",
            "salary": 60000,
        },
    )

    assert response.status_code == 409



#### Parameterized test
import pytest

@pytest.mark.parametrize(
    "salary, expected_status",
    [
        (-1, 422),
        (0, 422),
        (0.01, 201),
        (1_000_000, 201),
        (1_000_001, 422),
    ],
)
def test_salary_boundaries(
    client,
    salary,
    expected_status,
):

    response = client.post(
        "/api/employees",
        json={
            "name": "Boundary Tester",
            "email": f"boundary{salary}@example.com",
            "salary": salary,
        },
    )

    assert response.status_code == expected_status



#### Mock dependencies in API Test
# let's understand when API-level mocking is useful.
# Suppose we want to test how the router behaves when the service raises EmployeeNotFoundError.
# We don't need a real database for this test.
# We can replace the service dependency with a mock service.

from unittest.mock import Mock

from app.main import app
from app.routers.employee_router import (
    get_employee_service,
)
from app.services.employee_service import (
    EmployeeNotFoundError,
)


def test_employee_api_handles_service_error():

    mock_service = Mock()

    mock_service.get_employee.side_effect = (
        EmployeeNotFoundError(
            "Employee 999 was not found."
        )
    )
############ What is side_effect?
### Calling mock_service.get_employee() raises the specified exception.
### This lets us test exception handling without requiring a real missing employee in a database.


    def override_service():

        return mock_service

    app.dependency_overrides[
        get_employee_service
    ] = override_service
### Because this test focuses on router behavior.
### Replacing the service isolates the router from the database and repository.
### This makes it easier to verify that the router correctly translates a service exception into an HTTP response.

    try:

        from fastapi.testclient import TestClient

        with TestClient(app) as test_client:

            response = test_client.get(
                "/api/employees/999"
            )

        assert response.status_code == 404

        assert response.json()["detail"] == (
            "Employee 999 was not found."
        )

    finally:

        app.dependency_overrides.clear()



    '''
What is TestClient?
```````````````````
FastAPI provides TestClient for testing an application without starting a separate HTTP server.

For example:

response = client.get("/api/employees")

This sends a test request to the application.
It does not require you to run Uvicorn in another terminal.


Why use client.post()?
```````````````````````
response = client.post(
    "/api/employees",
    json=payload,
)

This simulates an HTTP POST request with a JSON request body.

FastAPI receives the request, validates the Pydantic schema, invokes the service, accesses the test database, and generates the response.
====================================================

Why call response.json()?
`````````````````````````
body = response.json()

This converts the JSON response body into a Python dictionary or list.
You can then assert individual values.


What does this test verify?
````````````````````````````
assert response.status_code == 201
Verifies the HTTP status code.

assert body["email"] == "arun@example.com"
Verifies the returned data.

assert body["employee_id"] > 0
Verifies that the database-generated identifier was returned.

Together, these assertions verify more than just whether the endpoint is reachable.


*********************************************
*********************************************

Negative testing
******************
Negative testing verifies that invalid input or invalid operations are rejected correctly.


Why expect HTTP 422?
--------------------
FastAPI uses Pydantic to validate the incoming request body.

If the email or salary violates the declared schema, the request is rejected before the endpoint's business logic executes.

FastAPI normally returns 422 Unprocessable Entity for these request validation errors.


Why expect HTTP 409 for duplicate email?
----------------------------------------
HTTP 409 indicates a conflict with the current state of the resource.

Our service detects the existing email and raises DuplicateEmailError.

The router converts this into an HTTP 409 response.

The database constraint provides additional protection against duplicate records caused by concurrent requests.

**********************************************

Boundary testing
*****************
Boundary testing checks the minimum and maximum permitted values.

Our employee schema defines:

salary: float = Field(
    gt=0,
    le=1_000_000,
)

The accepted range is:
0 < salary <= 1,000,000

The important boundary cases are:
`````````````````````````````````
Salary	        Expected result	        Reason
``````````````````````````````````````````````````````````````````
-1	            Reject	                Below the valid range
0	            Reject	                Salary must be greater than zero
0.01	        Accept	                Positive value
1,000,000	    Accept	                Maximum permitted value
1,000,001	    Reject	                Above the maximum

**************************************************************************

What is pytest.mark.parametrize()?
``````````````````````````````````
It runs the same test with multiple sets of input values.

Instead of writing five separate functions, we write one parameterized test.

Each test case gets its own client fixture, which creates a clean database state.

Training takeaway: Boundary testing is not limited to numeric values. It also applies to string lengths, pagination limits, dates, file sizes, and collection counts.


****************************************************************************

Mocking Dependencies in API Tests
**************************************

We already used mocks in our unit tests.

Now let's understand when API-level mocking is useful.

Suppose we want to test how the router behaves when the service raises EmployeeNotFoundError.

We don't need a real database for this test.

We can replace the service dependency with a mock service.

Add this test to tests/api/test_employee_api.py.

------------------------------

What is side_effect?
````````````````````
In this example:

mock_service.get_employee.side_effect = (
    EmployeeNotFoundError(...)
)

Calling mock_service.get_employee() raises the specified exception.
This lets us test exception handling without requiring a real missing employee in a database.


Why override get_employee_service rather than get_db?
```````````````````````````````````````````````````````
Because this test focuses on router behavior.

Replacing the service isolates the router from the database and repository.

This makes it easier to verify that the router correctly translates a service exception into an HTTP response.


Corporate testing principle
```````````````````````````
Use dependency overrides when testing application wiring and HTTP behavior with controlled dependencies.

Use the real database when you need to verify persistence or database integration.
    '''


