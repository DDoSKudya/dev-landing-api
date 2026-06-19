from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import engine
from app.core.error_handlers import register_error_handlers
from app.core.logging import setup_logging
from app.core.middleware import DbSessionMiddleware, RequestLoggingMiddleware
from app.contact.router import router as contact_router
from app.health.router import router as health_router
from app.metrics.router import router as metrics_router


@asynccontextmanager
async def lifespan(_app: FastAPI):
    settings.resolved_data_dir.mkdir(parents=True, exist_ok=True)
    yield
    await engine.dispose()


def create_app() -> FastAPI:
    setup_logging()

    app = FastAPI(title=settings.app_name, lifespan=lifespan)
    register_error_handlers(app)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(DbSessionMiddleware)

    app.include_router(health_router, prefix="/api")
    app.include_router(contact_router, prefix="/api")
    app.include_router(metrics_router, prefix="/api")
    return app


app = create_app()
