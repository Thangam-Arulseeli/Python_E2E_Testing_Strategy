### Create the API Router   -- Create app/routers/employee_router.py

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repositories.employee_repository import (
    EmployeeRepository,
    DuplicateEmailError,
)
from app.schemas.employee import EmployeeCreate, EmployeeResponse, EmployeeUpdate
from app.services.employee_service import (
    EmployeeNotFoundError,
    EmployeeService,
)


router = APIRouter(
    prefix="/api/employees",
    tags=["Employees"],
)


def get_employee_service(
    db: Annotated[Session, Depends(get_db)],
) -> EmployeeService:

    repository = EmployeeRepository(db)
    return EmployeeService(repository)


EmployeeServiceDependency = Annotated[
    EmployeeService,
    Depends(get_employee_service),
]


@router.post(
    "",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_employee(
    data: EmployeeCreate,
    service: EmployeeServiceDependency,
):

    try:
        return service.create_employee(data)

    except DuplicateEmailError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@router.get(
    "",
    response_model=list[EmployeeResponse],
)
def get_employees(
    service: EmployeeServiceDependency,
):

    return service.get_all_employees()



@router.get(
    "/{employee_id}",
    response_model=EmployeeResponse,
)
def get_employee(
    employee_id: int,
    service: EmployeeServiceDependency,
):

    try:
        return service.get_employee(employee_id)

    except EmployeeNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc



@router.put(
    "/{employee_id}",
    response_model=EmployeeResponse,
)
def update_employee(
    employee_id: int,
    data: EmployeeUpdate,
    service: EmployeeServiceDependency,
):

    try:
        return service.update_employee(employee_id, data)

    except EmployeeNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    except DuplicateEmailError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc



@router.delete(
    "/{employee_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_employee(
    employee_id: int,
    service: EmployeeServiceDependency,
):

    try:
        service.delete_employee(employee_id)

    except EmployeeNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    return Response(status_code=status.HTTP_204_NO_CONTENT)


'''
Concepts demonstrated
-----------------------
Dependency injection
``````
Depends(get_employee_service)

FastAPI creates the service through the dependency function.


Exception translation
---------------------
raise HTTPException(
    status_code=404,
    detail=str(exc),
)

The router converts an application-level exception into an HTTP response.

Response models
---------------
response_model=EmployeeResponse

FastAPI validates and serializes the returned data according to the response schema.
'''