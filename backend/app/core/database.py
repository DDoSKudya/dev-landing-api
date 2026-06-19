import logging
from contextlib import asynccontextmanager
from contextvars import ContextVar

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

logger = logging.getLogger(__name__)

_session_ctx: ContextVar[AsyncSession | None] = ContextVar("db_session", default=None)

engine = create_async_engine(settings.database_url, echo=settings.debug)
async_session_factory = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


def get_session() -> AsyncSession:
    session = _session_ctx.get()
    if session is None:
        raise RuntimeError(
            "Database session is not active. Wrap the operation in "
            "`async with session_scope():` or enable DbSessionMiddleware."
        )
    return session


@asynccontextmanager
async def session_scope():
    session = async_session_factory()
    token = _session_ctx.set(session)
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()
        _session_ctx.reset(token)


async def check_database() -> bool:
    try:
        session = _session_ctx.get()
        if session is not None:
            await session.execute(text("SELECT 1"))
        else:
            async with async_session_factory() as standalone:
                await standalone.execute(text("SELECT 1"))
        return True
    except Exception:
        logger.warning("Database health check failed", exc_info=True)
        return False
