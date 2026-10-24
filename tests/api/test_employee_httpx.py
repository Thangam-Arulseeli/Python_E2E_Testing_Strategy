'''
Direct HTTPX Testing  -- Create tests/api/test_employee_httpx.py
``````````````````````````````````````````````````````````````````
FastAPI's TestClient is convenient for synchronous tests.

However, HTTPX can also be used directly with an ASGI application.

This is particularly useful when testing asynchronous applications.

First, understand the difference.

Feature	                    TestClient	             HTTPX AsyncClient
````````````````````````````````````````````````````````````````````````````
Main interface	            Synchronous	             Asynchronous
Request methods	            client.get()	         await client.get()
Starts a network server	    No	                     No, when using ASGITransport
Good for	                Most simple API tests	 Async test workflows
Requires pytest-asyncio	    No	                     Yes, for the example below


Install the additional dependency:
    python -m pip install pytest-asyncio

Add it to requirements.txt:

pytest-asyncio

'''

import pytest

from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.asyncio   ### Allows Pytest to execute the asynchronous test using the pytest-asyncio plugin.
async def test_root_endpoint_with_httpx():

    transport = ASGITransport(app=app) # Connects HTTPX directly to the ASGI application without starting a real web server.

    async with AsyncClient(   ### Creates an asynchronous HTTP client.
        transport=transport,
        base_url="http://test",
    ) as client:

        response = await client.get("/")  ### Sends the request asynchronously.

    assert response.status_code == 200

    assert response.json() == {
        "message": "Employee Management API is running"
    }


'''
Important note about database-dependent HTTPX tests
----------------------------------------------------
This example tests only the root endpoint, so it doesn't require the test database.

If you use AsyncClient to test employee endpoints, you must apply the same database dependency override as in the TestClient tests.

Also, when an application relies on lifespan startup or shutdown logic, configure lifespan management explicitly in asynchronous tests when needed. ASGITransport does not automatically run application lifespan events.
'''


'''
Explanation
------------
ASGITransport
`````
transport = ASGITransport(app=app)
Connects HTTPX directly to the ASGI application without starting a real web server.


AsyncClient
`````
async with AsyncClient(...) as client:
Creates an asynchronous HTTP client.


await client.get("/")
Sends the request asynchronously.


@pytest.mark.asyncio
Allows Pytest to execute the asynchronous test using the pytest-asyncio plugin.


Important note about database-dependent HTTPX tests
----------------------------------------------------
This example tests only the root endpoint, so it doesn't require the test database.

If you use AsyncClient to test employee endpoints, you must apply the same database dependency override as in the TestClient tests.

Also, when an application relies on lifespan startup or shutdown logic, configure lifespan management explicitly in asynchronous tests when needed. ASGITransport does not automatically run application lifespan events.
'''
