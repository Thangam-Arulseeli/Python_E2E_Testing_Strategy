### Create tests/integration/test_employee_repository.py
import pytest

from app.repositories.employee_repository import (
    EmployeeRepository,
)
from app.schemas.employee import EmployeeCreate


def test_create_employee_in_database(db_session):

    repository = EmployeeRepository(db_session)

    data = EmployeeCreate(
        name="Priya Sharma",
        email="priya@example.com",
        salary=60000,
    )

    created_employee = repository.create(data)

    assert created_employee.employee_id is not None
    assert created_employee.name == "Priya Sharma"
    assert created_employee.email == "priya@example.com"
    assert created_employee.salary == 60000

    saved_employee = repository.get_by_id(
        created_employee.employee_id
    )

    assert saved_employee is not None
    assert saved_employee.name == "Priya Sharma"


def test_list_employees(db_session, sample_employee):

    repository = EmployeeRepository(db_session)

    employees = repository.get_all()

    assert len(employees) == 1

    assert employees[0].employee_id == (
        sample_employee.employee_id
    )


def test_duplicate_email_is_rejected(db_session):

    repository = EmployeeRepository(db_session)

    first_employee = EmployeeCreate(
        name="Arun Kumar",
        email="arun@example.com",
        salary=50000,
    )

    second_employee = EmployeeCreate(
        name="Arun Raj",
        email="arun@example.com",
        salary=60000,
    )

    repository.create(first_employee)

    with pytest.raises(Exception) as error:

        repository.create(second_employee)

    assert "already exists" in str(error.value)


'''
Integration Testing
***********************
What is integration testing?
`````````````````````````````
Integration testing verifies that different components work together correctly.

For our application, we want to confirm that:
```````````````````````````````````````````````
The repository receives employee data.
SQLAlchemy creates the corresponding database record.
The database stores the values.
A subsequent query retrieves the record correctly.

Unlike unit tests, these tests use a real database engine.

We will use the SQLite test database.

*************************************************

Important improvement for training
======================================
The third test should assert the specific exception rather than the generic Exception class.

Replace the generic assertion with:

from app.repositories.employee_repository import (
    DuplicateEmailError,
)

with pytest.raises(DuplicateEmailError):
    repository.create(second_employee)

This makes the test more precise.


What does this integration test prove?
======================================
It verifies that the repository:

Creates an ORM object.
Persists it to the database.
Commits the transaction.
Refreshes the object.
Retrieves the saved record.
Handles database uniqueness errors.

A mocked repository cannot prove these database operations work correctly. That's why we need integration tests.

'''