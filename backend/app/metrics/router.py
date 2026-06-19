from fastapi import APIRouter, Query

from app.metrics.schemas import MetricsResponse
from app.metrics.service import get_metrics

router = APIRouter(tags=["metrics"])


@router.get("/metrics", response_model=MetricsResponse)
async def metrics(days: int = Query(default=30, ge=1, le=365)) -> MetricsResponse:
    return await get_metrics(days)
