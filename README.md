Professional Testing Strategy in FastAPI -- Employee Management API
*********************************************************************

We will build a complete Employee Management API using FastAPI, SQLAlchemy, Pydantic, Pytest, HTTPX, and SQLite as a dedicated test database.

We will cover:

Professional testing strategy
Unit testing
Integration testing
API testing
FastAPI TestClient
HTTPX
Pytest fixtures
Mocking dependencies
Dependency overrides
Dedicated test database
Positive, negative, and boundary testing
Test coverage
Step-by-step execution
Corporate best practices
================================================

Technologies Used
----------------------
We will use the following technologies.

Technology	            Purpose
------------------------------------------------------------
Python	                Programming language
FastAPI	                Build REST APIs
Pydantic	            Validate request and response data
SQLAlchemy 2.x	        Database access and ORM
SQLite	                Dedicated test database
Pytest	                Execute and organize tests
HTTPX	                Send HTTP requests asynchronously or synchronously
FastAPI TestClient	    Test API endpoints conveniently
pytest-cov	            Measure test coverage
===================================================================

Project Requirements
-----------------------
Our practical project will implement these endpoints.

HTTP method	            Endpoint	                    Purpose	                Expected status
------------------------------------------------------------------------------------------------
POST	                /api/employees	                Create an employee	    201
GET	                    /api/employees	                List employees	        200
GET	                    /api/employees/{employee_id}	Retrieve an employee	200
PUT	                    /api/employees/{employee_id}	Update an employee	    200
DELETE	                /api/employees/{employee_id}	Delete an employee	    204

We will also test:

Missing employee IDs
Duplicate emails
Invalid email addresses
Invalid salaries
Empty employee names
Boundary values
Database isolation between tests
Service behavior using mocks
Test coverage

================================================================


Create the Project Folder Structure
--------------------------------------------
Create a project named Python_E2E_Testing_Strategy

Use the following structure:

Python_E2E_Testing_Strategy/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   └── session.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── employee.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── employee.py
│   │
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── employee_repository.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   └── employee_service.py
│   │
│   └── routers/
│       ├── __init__.py
│       └── employee_router.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   │
│   ├── unit/
│   │   ├── __init__.py
│   │   └── test_employee_service.py
│   │
│   ├── integration/
│   │   ├── __init__.py
│   │   └── test_employee_repository.py
│   │
│   └── api/
│       ├── __init__.py
│       └── test_employee_api.py
│
├── .env
├── .gitignore
├── pytest.ini
└── requirements.txt


Why separate the tests into folders?
`````````````````````````````````````````
unit/:              Tests individual components without a real database.
integration/:       Tests the interaction between components and a real test database.
api/:               Tests HTTP requests, responses, routing, and validation.
conftest.py:        Contains shared fixtures used by multiple test modules.

This structure helps teams maintain a growing test suite.
===============================================================

Install the Dependencies
-------------------------
Create requirements.txt.

fastapi
uvicorn[standard]
sqlalchemy>=2.0,<3.0
pydantic[email]
python-dotenv
pytest
httpx
pytest-cov
=====================================

Create a virtual environment.
-----------------------------

Open PowerShell in the project directory.
    > python -m venv .venv

Activate it:
    > .\.venv\Scripts\Activate.ps1

Install the packages:
    python -m pip install -r requirements.txt

Verify the installation:
    > python -m pytest --version


Why use python -m pytest?
`````````````````````````````
It runs Pytest through the currently selected Python interpreter. This helps avoid the common problem of the pytest command not being recognized when packages are installed in a different environment.
========================================================

Configure the Application
-------------------------------
Create app/core/config.py.

import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./employees.db",
)


Create .env.
--------------
DATABASE_URL=sqlite:///./employees.db

Explanation
```````````
The application reads its database URL from the environment.

For normal development, it defaults to:

sqlite:///./employees.db

Our tests will override the database dependency and use a separate SQLite database.

Professional rule: Tests must never accidentally connect to or modify a production database.

For a real deployment, validate database configuration at startup and use environment-specific secrets rather than committing credentials to source control.
==============================================================

Configure SQLAlchemy
--------------------
Create app/database/session.py
========================================================

Create the Employee Model
``````````````````````````
Create app/models/employee.py
========================================================


Create Pydantic Schemas
------------------------
Create app/schemas/employee.py
=======================================================


Create the Repository Layer
----------------------------
Create app/repositories/employee_repository.py.
=====================================================


Create the Service Layer
-------------------------
Create app/services/employee_service.py.
====================================================

Create the API Router
----------------------
Create app/routers/employee_router.py

====================================================
****************************************************

Configure Pytest
----------------
Create pytest.ini.

[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -ra

What does this configuration do?
````````````````````````````````````
Setting                     	Purpose
-----------------------------------------
testpaths	                    Specifies the test directory
python_files	                Identifies test files
python_classes	                Identifies test classes
python_functions	            Identifies test functions
-ra	                            Displays additional information about skipped or failed tests

******************************

'''
Now we can run all tests from the project root:
    > python -m pytest

NOTE: Bbefore writing the tests, we need shared fixtures.
'''

************************************************************


Create Pytest Fixtures and a Dedicated Test Database
````````````````````````````````````````````````````
Create tests/conftest.py.

============================================================

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

Create tests/unit/test_employee_service.py
===============================================================


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

Create tests/integration/test_employee_repository.py.
===========================================================


API Testing with FastAPI TestClient
************************************

Now we will test the application through HTTP requests.

Create tests/api/test_employee_api.py.

=========================================================

Positive, Negative, and Boundary Testing
********************************************
A professional test suite must verify valid input, invalid input, and values at the edges of allowed ranges.

These categories are especially important for APIs that receive user input.

Positive testing
*****************
Positive testing verifies that valid input is accepted.

Example:

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

Expected result: The employee is created successfully.


*******************************************
*******************************************
*******************************************

Mocking Dependencies in API Tests
***********************************
We already used mocks in our unit tests.

Now let's understand when API-level mocking is useful.

Suppose we want to test how the router behaves when the service raises EmployeeNotFoundError.

We don't need a real database for this test.

We can replace the service dependency with a mock service.

Add this test to tests/api/test_employee_api.py.

********************************************************************************************
********************************************************************************************

Test Database Isolation
************************

Database isolation means that one test should not accidentally depend on records created by another test.

Consider these tests:

def test_create_employee_success(client):
    ...


And:


def test_list_employees(client):
    ...

If the first test leaves records in the database, the second test may become dependent on test execution order.

That is undesirable.


Our fixture solves this by recreating the schema for each test.
``````````````````````````````````````````````````````````````
@pytest.fixture
def db_session():

    Base.metadata.create_all(bind=test_engine)

    db = TestingSessionLocal()

    try:
        yield db

    finally:
        db.close()
        Base.metadata.drop_all(bind=test_engine)


How does it work?
`````````````````````
Create the tables.
Open a session.
Execute the test.
Close the session.
Drop the tables.

The next test starts with a clean schema.


What about production databases?
````````````````````````````````
Never run drop_all() against a production database.

For a production-grade test suite, consider:

A dedicated test database.
A disposable database created for the test run.
Transaction rollback fixtures.
Database containers.
Schema migrations before running integration tests.
A separate PostgreSQL instance for PostgreSQL-specific behavior.

Our SQLite setup is useful for fast training tests

But it does not reproduce every PostgreSQL behavior.

=======================================================================


Measure Test Coverage
***********************
Test coverage helps us understand how much application code our tests execute.

Install pytest-cov if you have not already done so.

Run:

python -m pytest --cov=app --cov-report=term-missing

This produces a coverage report.


The report typically includes:
```````````````````````````````
Column	Meaning
`````````````````````````````````
Name	Source file
Stmts	Number of executable statements
Miss	Statements not executed
Cover	Percentage of statements executed


To generate an HTML report:

    > python -m pytest --cov=app --cov-report=html

After the command finishes, open:

    > htmlcov/index.html

The report shows which lines of code were executed during the tests.


What is 100% coverage?
```````````````````````
100% statement coverage means all measured executable statements were executed.

It does not guarantee that the application is bug-free.

For example, this code might execute during a test:

if salary > 0:
    return True

But if you only test a positive salary, you haven't tested the false branch.

Therefore, branch coverage can provide additional insight.


Run:

python -m pytest --cov=app --cov-branch --cov-report=term-missing

Professional recommendation
``````````````````````````````
Do not chase coverage percentages without checking test quality.

A smaller suite that tests important business rules, error handling, and boundary conditions is often more valuable than a larger suite that merely executes lines.
=============================================================================
******************************************************************************

Run the Entire Test Suite
=========================
Once all files are created, execute the tests from the project root.

    > python -m pytest -v


The -v option displays each test name and its result.

The output should resemble:

tests/unit/test_employee_service.py::test_get_employee_success PASSED
tests/unit/test_employee_service.py::test_get_employee_not_found PASSED
tests/unit/test_employee_service.py::test_create_employee_success PASSED
tests/unit/test_employee_service.py::test_create_duplicate_email PASSED

tests/integration/test_employee_repository.py::test_create_employee_in_database PASSED
tests/integration/test_employee_repository.py::test_list_employees PASSED
tests/integration/test_employee_repository.py::test_duplicate_email_is_rejected PASSED

tests/api/test_employee_api.py::test_create_employee_success PASSED
tests/api/test_employee_api.py::test_get_employee_success PASSED
tests/api/test_employee_api.py::test_get_employee_not_found PASSED
tests/api/test_employee_api.py::test_list_employees PASSED
tests/api/test_employee_api.py::test_update_employee PASSED
tests/api/test_employee_api.py::test_delete_employee PASSED

==================== test session summary ====================

The output above is illustrative. The actual number of tests and results will depend on the files you have created and your installed package versions.

If any test fails, Pytest will display the failure details.

Run only unit tests     -->  python -m pytest tests/unit -v
Run only integration tests  -->  python -m pytest tests/integration -v
Run only API tests      -->  python -m pytest tests/api -v
Stop after the first failure    -->  python -m pytest -x
Show print statements and other captured output     -->   python -m pytest -s
Run a single test       -->  
     python -m pytest tests/api/test_employee_api.py::test_create_employee_success -v

These commands are useful when debugging test failures during training.

==================================================================


Run the Application Separately
********************************
The test suite does not require a running Uvicorn server.

However, you can start the application to verify its behavior manually.

Run:

python -m uvicorn app.main:app --reload

Open the Swagger UI:

http://127.0.0.1:8000/docs

You can test the endpoints interactively.

For example, send a request to:

POST /api/employees

With this JSON body:

{
  "name": "Arun Kumar",
  "email": "arun@example.com",
  "salary": 50000
}

Expected response:

{
  "employee_id": 1,
  "name": "Arun Kumar",
  "email": "arun@example.com",
  "salary": 50000.0
}

The actual employee ID depends on the database contents.

Remember: Swagger testing is manual API testing. Pytest and TestClient provide repeatable automated testing.
==========================================================================


Understanding the Complete Testing Workflow
*********************************************
Here is the workflow you should teach trainees.

                  REQUIREMENTS
                       |
                       v
               IDENTIFY TEST CASES
                       |
                       v
                WRITE UNIT TESTS
                       |
                       v
             WRITE INTEGRATION TESTS
                       |
                       v
                 WRITE API TESTS
                       |
                       v
            EXECUTE THE TEST SUITE
                       |
                       v
             ANALYZE FAILED TESTS
                       |
                       v
              FIX APPLICATION CODE
                       |
                       v
               RE-RUN ALL TESTS
                       |
                       v
               MEASURE COVERAGE
                       |
                       v
               REVIEW TEST QUALITY

For a professional team, testing should be performed continuously rather than only at the end of development.

A typical pull request workflow includes:

Developer writes or modifies application code.
Developer writes or updates tests.
Automated tests run locally.
Code is pushed to the repository.
A CI pipeline runs the tests.
Failed tests block merging according to team policy.
Approved code is merged and deployed through the normal release process.
===============================================================

