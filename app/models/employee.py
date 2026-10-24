### Create the Employee Model   --  Create app/models/employee.py

from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped, mapped_column

from app.database.session import Base


class Employee(Base):

    __tablename__ = "employees"

    employee_id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )

    salary: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )


'''
What does this model represent?
````````````````````````````````
It maps a Python class to a database table.

The table will have these columns:

Column	        Type	    Constraint
```````````````````````````````````````````
employee_id	    Integer	    Primary key
name	        String	    Not null
email	        String	    Unique, not null
salary	        Float	    Not null


The database-level unique constraint on email protects against duplicate emails even if application-level validation is bypassed.

We will also validate employee input using Pydantic.

For financial applications, use an appropriate decimal-based database and Python type rather than floating-point salary storage. We use Float here to keep the training example simple.
'''