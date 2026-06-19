from datetime import UTC, datetime

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.core.database import check_database

router = APIRouter(tags=["health"])


@router.get("/health")
async def health() -> JSONResponse:
    db_ok = await check_database()
    body = {
        "status": "ok" if db_ok else "degraded",
        "version": "0.1.0",
        "timestamp": datetime.now(UTC).isoformat(),
        "checks": {"database": "ok" if db_ok else "error"},
    }
    return JSONResponse(status_code=200 if db_ok else 503, content=body)
