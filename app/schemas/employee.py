### Create Pydantic Schemas  -- Create app/schemas/employee.py

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class EmployeeCreate(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=100,
    )

    email: EmailStr

    salary: float = Field(
        gt=0,
        le=1_000_000,
    )


class EmployeeUpdate(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=100,
    )

    email: EmailStr

    salary: float = Field(
        gt=0,
        le=1_000_000,
    )


class EmployeeResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)  # allows Pydantic to build a response model from SQLAlchemy ORM objects

    employee_id: int
    name: str
    email: EmailStr
    salary: float


'''
What are we validating?
-------------------------
Field	    Validation rule
Name	    Between 2 and 100 characters
Email	    Must be a valid email address
Salary	    Greater than 0 and at most 1,000,000

These rules create useful positive, negative, and boundary test cases.


For example:

Salary  50000:      Valid.
Salary  0:          Invalid.
Salary  -100:       Invalid.
Salary  1000000:    Valid.
Salary  1000001:    Invalid.

The schema performs request validation before the router executes the endpoint function.

from_attributes=True allows Pydantic to build a response model from SQLAlchemy ORM objects.
'''
