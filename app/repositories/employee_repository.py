### Create the Repository Layer -- Create app/repositories/employee_repository.py

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate


class DuplicateEmailError(Exception):
    pass


class EmployeeRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, data: EmployeeCreate) -> Employee:

        employee = Employee(
            name=data.name,
            email=str(data.email),
            salary=data.salary,
        )

        self.db.add(employee)

        try:
            self.db.commit()
            self.db.refresh(employee)

        except IntegrityError as exc:
            self.db.rollback()

            raise DuplicateEmailError(
                "An employee with this email already exists."
            ) from exc

        return employee



    def get_by_id(self, employee_id: int):

        statement = select(Employee).where(
            Employee.employee_id == employee_id
        )

        return self.db.scalars(statement).first()



    def get_by_email(self, email: str):

        statement = select(Employee).where(
            Employee.email == email
        )

        return self.db.scalars(statement).first()



    def get_all(self):

        statement = select(Employee).order_by(
            Employee.employee_id
        )

        return self.db.scalars(statement).all()



    def update(
        self,
        employee: Employee,
        data: EmployeeUpdate,
    ) -> Employee:

        employee.name = data.name
        employee.email = str(data.email)
        employee.salary = data.salary

        try:
            self.db.commit()
            self.db.refresh(employee)

        except IntegrityError as exc:
            self.db.rollback()

            raise DuplicateEmailError(
                "An employee with this email already exists."
            ) from exc

        return employee


    def delete(self, employee: Employee) -> None:

        self.db.delete(employee)
        self.db.commit()


'''
What is the repository responsible for?
`````````````````````````````````````````
The repository manages database operations.

It knows how to:

Insert an employee.
Retrieve an employee.
List employees.
Update an employee.
Delete an employee.

It does not decide whether a salary is valid or whether an employee ID should produce an HTTP 404 response.

Those responsibilities belong to other layers.


Why is rollback() important?
-----------------------------
Suppose inserting an employee fails because the email violates a database constraint.

The session enters a failed transaction state.

Calling:

self.db.rollback()

resets the transaction so that the session can be used safely again.

Our code converts the database constraint error into a domain-specific exception.
'''

