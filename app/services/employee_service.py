### Create the Service Layer    --- Create app/services/employee_service.py

from app.repositories.employee_repository import (
    EmployeeRepository,
    DuplicateEmailError,
)
from app.schemas.employee import EmployeeCreate, EmployeeUpdate


class EmployeeNotFoundError(Exception):
    pass


class EmployeeService:

    def __init__(self, repository: EmployeeRepository):
        self.repository = repository

    def create_employee(self, data: EmployeeCreate):

        if self.repository.get_by_email(str(data.email)):
            raise DuplicateEmailError(
                "An employee with this email already exists."
            )

        return self.repository.create(data)

   
    def get_employee(self, employee_id: int):

        employee = self.repository.get_by_id(employee_id)

        if employee is None:
            raise EmployeeNotFoundError(
                f"Employee {employee_id} was not found."
            )

        return employee


    def get_all_employees(self):

        return self.repository.get_all()


    def update_employee(
        self,
        employee_id: int,
        data: EmployeeUpdate,
    ):

        employee = self.get_employee(employee_id)

        if str(data.email) != employee.email:
            existing = self.repository.get_by_email(
                str(data.email)
            )

            if existing is not None:
                raise DuplicateEmailError(
                    "An employee with this email already exists."
                )

        return self.repository.update(employee, data)


    def delete_employee(self, employee_id: int):

        employee = self.get_employee(employee_id)
        if employee is None:
            raise EmployeeNotFoundError(
                 f"Employee {employee_id} was not found."
                    )
        self.repository.delete(employee)


'''
Why separate the service and repository?
````````````````````````````````````````
The service contains application and business logic.

The repository contains database access logic.

For example:

employee = self.repository.get_by_id(employee_id)

if employee is None:
    raise EmployeeNotFoundError(...)

The service decides what it means when an employee does not exist.

The router will translate this exception into an HTTP response.

Important corporate consideration: The pre-check for duplicate email improves the error message, but it cannot prevent concurrent requests from inserting the same email. The database unique constraint remains essential.
'''


