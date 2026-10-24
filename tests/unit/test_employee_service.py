from unittest.mock import Mock

import pytest

from app.schemas.employee import EmployeeCreate
from app.services.employee_service import (
    EmployeeNotFoundError,
    EmployeeService,
)
from app.repositories.employee_repository import (
    DuplicateEmailError,
)


def test_get_employee_success():

    repository = Mock()

    expected_employee = Mock()
    expected_employee.employee_id = 1
    expected_employee.name = "Arun Kumar"

    repository.get_by_id.return_value = expected_employee  # Configures the mock to return a particular employee.

    service = EmployeeService(repository) # Injects the mock repository into the service.

    result = service.get_employee(1)   # Executes the real service method

    assert result.employee_id == 1      # Verifies the result.
    assert result.name == "Arun Kumar"

    repository.get_by_id.assert_called_once_with(1) # Verifies that the service called the repository with the correct ID exactly once.
## This assertion checks the interaction between the service and its dependency.


def test_get_employee_not_found():

    repository = Mock()

    repository.get_by_id.return_value = None

    service = EmployeeService(repository)

    with pytest.raises(EmployeeNotFoundError):

        service.get_employee(999)

### This test passes only when the expected exception is raised.
        # If no exception is raised, the test fails.
        # Unit tests help verify both normal and exceptional business logic.



def test_create_employee_success():

    repository = Mock()

    repository.get_by_email.return_value = None

    expected_employee = Mock()
    expected_employee.employee_id = 1
    expected_employee.name = "Arun Kumar"

    repository.create.return_value = expected_employee

    service = EmployeeService(repository)

    data = EmployeeCreate(
        name="Arun Kumar",
        email="arun@example.com",
        salary=50000,
    )

    result = service.create_employee(data)

    assert result.employee_id == 1

    repository.get_by_email.assert_called_once_with(
        "arun@example.com"
    )

    repository.create.assert_called_once_with(data)



def test_create_duplicate_email():

    repository = Mock()

    existing_employee = Mock()

    repository.get_by_email.return_value = existing_employee

    service = EmployeeService(repository)

    data = EmployeeCreate(
        name="Arun Kumar",
        email="arun@example.com",
        salary=50000,
    )

    with pytest.raises(DuplicateEmailError):

        service.create_employee(data)

    repository.create.assert_not_called()



    '''
Unit Testing
*****************
What is unit testing?
---------------------
Unit testing verifies an individual component independently of external systems.

For example, we want to verify:

What happens when an employee exists.
What happens when an employee does not exist.
Whether a duplicate email raises the correct exception.
Whether the service calls the repository correctly.

We do not need FastAPI or a database to test these business rules.

We can use mocks.


What is mocking?
`````````````````
Mocking replaces a real dependency with a controlled test object.

For example, instead of querying a database, we configure a mock repository to return a known employee.

This makes the test fast and independent of database setup.

================================================

Explanation of the first unit test
***********************************

repository = Mock()     ### Creates a mock object.

repository.get_by_id.return_value = expected_employee
Configures the mock to return a particular employee.

service = EmployeeService(repository)
Injects the mock repository into the service.

result = service.get_employee(1)
Executes the real service method.

assert result.employee_id == 1
Verifies the result.

repository.get_by_id.assert_called_once_with(1)
Verifies that the service called the repository with the correct ID exactly once.

This last assertion checks the interaction between the service and its dependency.
======================================================

What does pytest.raises() do?
```````````````````````````````
Consider:

with pytest.raises(EmployeeNotFoundError):
    service.get_employee(999)

This test passes only when the expected exception is raised.

If no exception is raised, the test fails.
Unit tests help verify both normal and exceptional business logic.

    '''