from datetime import UTC, datetime, timedelta

from app.contact.models import ContactSubmission
from app.metrics import repository
from app.metrics.schemas import MetricsResponse


async def get_metrics(days: int) -> MetricsResponse:
    since = datetime.now(UTC) - timedelta(days=days)
    submissions = await repository.list_submissions_since(since)
    return _aggregate(submissions)


def _aggregate(submissions: list[ContactSubmission]) -> MetricsResponse:
    by_category: dict[str, int] = {}
    by_sentiment: dict[str, int] = {}
    ai_unavailable_count = 0

    for submission in submissions:
        if submission.request_category:
            key = submission.request_category
            by_category[key] = by_category.get(key, 0) + 1
        if submission.sentiment:
            key = submission.sentiment
            by_sentiment[key] = by_sentiment.get(key, 0) + 1
        if submission.ai_status == "unavailable":
            ai_unavailable_count += 1

    return MetricsResponse(
        total=len(submissions),
        by_category=by_category,
        by_sentiment=by_sentiment,
        ai_unavailable_count=ai_unavailable_count,
    )
