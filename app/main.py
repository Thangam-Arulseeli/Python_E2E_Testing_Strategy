from fastapi import FastAPI

from app.database.session import Base, engine
from app.models.employee import Employee
from app.routers.employee_router import router as employee_router


app = FastAPI(
    title="Employee Management API",
    version="1.0.0",
)


# Suitable for this simple training application.
# Production applications should generally use migrations.
Base.metadata.create_all(bind=engine)


app.include_router(employee_router)


@app.get("/")
def root():

    return {
        "message": "Employee Management API is running"
    }


'''
The Employee import ensures the model is registered in SQLAlchemy metadata before create_all() executes.

create_all() creates missing tables, but it does not manage schema changes like a migration tool.

For a production application, use database migrations and avoid relying on create_all() as a deployment migration strategy.
'''
