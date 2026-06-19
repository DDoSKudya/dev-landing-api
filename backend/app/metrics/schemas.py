from pydantic import BaseModel


class MetricsResponse(BaseModel):
    total: int
    by_category: dict[str, int]
    by_sentiment: dict[str, int]
    ai_unavailable_count: int
