import os
import tempfile
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

os.environ["DATA_DIR"] = tempfile.mkdtemp()

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncConnection

from app.contact.models import ContactSubmission
from app.core.database import Base, engine
from app.main import app


@asynccontextmanager
async def open_test_connection() -> AsyncGenerator[AsyncConnection, None]:
    connection = await engine.connect()
    try:
        yield connection
    finally:
        await connection.close()


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    async with open_test_connection() as connection:
        async with connection.begin():
            await connection.run_sync(Base.metadata.create_all)
    try:
        yield
    finally:
        async with open_test_connection() as connection:
            async with connection.begin():
                await connection.run_sync(Base.metadata.drop_all)


@pytest.fixture(autouse=True)
async def clean_contact_submissions():
    yield
    async with open_test_connection() as connection:
        async with connection.begin():
            await connection.execute(delete(ContactSubmission))


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
