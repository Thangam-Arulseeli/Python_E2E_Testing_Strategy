### Create Pytest Fixtures and a Dedicated Test Database  -- Create tests/conftest.py.
### This file is one of the most important parts of our testing strategy

import pytest

from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database.session import Base, get_db
from app.main import app
from app.models.employee import Employee


TEST_DATABASE_URL = "sqlite://"  # sqlite:///:memory:  In-memory database
'''
Important: In our testing setup, StaticPool keeps the same in-memory database connection available to the test code. Our fixture creates the tables before a test and drops them afterward.

Therefore, you cannot open this test database in DB Browser for SQLite or another database viewer as a normal file.
'''


test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={
        "check_same_thread": False # allows multiple threads to access the same SQLite database connection simultaneously.
    },
    poolclass=StaticPool,   # This keeps the in-memory SQLite database available through the same connection pool, which is important because FastAPI's TestClient can execute endpoint code in a different thread.
    # Each test creates its tables and drops them afterward.
    # This gives us a lightweight, isolated database

# Using StaticPool allows the application and test setup to access the same in-memory database connection.
)


TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    expire_on_commit=False,
)


@pytest.fixture
def db_session():

    Base.metadata.create_all(bind=test_engine)

    db = TestingSessionLocal()

    try:
        yield db    # The object yielded is made available to the test.
                    # The code after yield performs cleanup when the test finishes.

    finally:
        db.close()
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def client(db_session):

    def override_get_db():

        yield db_session

    # During testing, we replace the dependency:
    app.dependency_overrides[get_db] = override_get_db # This makes API requests use the test database rather than the application's configured database.

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()  # After testing, restores the application to its normal dependency behavior.


@pytest.fixture
def sample_employee(db_session):

    employee = Employee(
        name="Arun Kumar",
        email="arun@example.com",
        salary=50000,
    )

    db_session.add(employee)
    db_session.commit()
    db_session.refresh(employee)

    return employee


'''
What is a Pytest fixture?
````````````````````````````
A fixture prepares resources that tests need.

For example:

@pytest.fixture
def client(db_session):
    ...

Any test that accepts client as an argument can use the configured test client.

###### Pytest automatically discovers and executes the fixture.

Example:

def test_example(client):
    response = client.get("/")
    assert response.status_code == 200

You do not need to call the fixture manually.
==========================================

What does yield do in a fixture?
````````````````````````````````
Consider:

@pytest.fixture
def db_session():

    db = TestingSessionLocal()

    try:
        yield db

    finally:
        db.close()

The code before yield prepares the resource.
The object yielded is made available to the test.
The code after yield performs cleanup when the test finishes.

This is especially useful for database sessions, files, temporary directories, and application clients.
====================================================

Why use SQLite in memory?
```````````````````````````
We configure:

TEST_DATABASE_URL = "sqlite://"

And:

poolclass=StaticPool

This keeps the in-memory SQLite database available through the same connection pool, which is important because FastAPI's TestClient can execute endpoint code in a different thread.

Each test creates its tables and drops them afterward.

This gives us a lightweight, isolated database for training.

Important: The fixture uses a shared session within a test. This is convenient for a small example, but more complex applications may need separate sessions per request and explicit transaction rollback strategies.

Also, this example assumes tests run sequentially. Do not run these shared in-memory database tests concurrently without redesigning the database fixture.
====================================================

What is dependency overriding?
```````````````````````````````
Our application normally uses:

Depends(get_db)

During testing, we replace the dependency:

app.dependency_overrides[get_db] = override_get_db
This makes API requests use the test database rather than the application's configured database.

After testing:

app.dependency_overrides.clear()
restores the application to its normal dependency behavior.

This is a fundamental FastAPI testing technique.
============================================================

Why use StaticPool?
`````````````````````
An in-memory SQLite database exists within a database connection.

Using StaticPool allows the application and test setup to access the same in-memory database connection.

Without suitable connection configuration, the test setup and API request may accidentally see different in-memory databases.
'''

