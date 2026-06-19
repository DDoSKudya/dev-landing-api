import os
import tempfile
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

os.environ["DATA_DIR"] = tempfile.mkdtemp()
os.environ["RATE_LIMIT_REQUESTS"] = "100"

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncConnection

from app.contact.models import ContactSubmission
from app.core.config import settings
from app.core.database import Base, engine
from app.core.rate_limit import RATE_LIMIT_FILE
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


@pytest.fixture(autouse=True)
def reset_rate_limit_file():
    yield
    rate_limit_path = settings.resolved_data_dir / RATE_LIMIT_FILE
    if rate_limit_path.exists():
        rate_limit_path.unlink()


@pytest.fixture(autouse=True)
def mock_contact_emails(monkeypatch):
    async def noop(*_args, **_kwargs):
        return None

    monkeypatch.setattr("app.contact.service.send_contact_emails", noop)


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
