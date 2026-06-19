import pytest

from app.contact.ai import AIResult
from tests.helpers import VALID_PAYLOAD, payload


@pytest.mark.parametrize(
    "days",
    [0, -1, 366, 1000],
    ids=["days_below_min", "days_negative", "days_above_max", "days_far_above_max"],
)
async def test_metrics_days_invalid_class(client, days):
    response = await client.get(f"/api/metrics?days={days}")
    assert response.status_code == 422


@pytest.mark.parametrize(
    "days",
    [1, 30, 365],
    ids=["days_boundary_min", "days_default_range", "days_boundary_max"],
)
async def test_metrics_days_valid_class(client, days):
    response = await client.get(f"/api/metrics?days={days}")
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 0
    assert body["by_category"] == {}
    assert body["by_sentiment"] == {}
    assert body["ai_unavailable_count"] == 0


async def test_metrics_empty_state(client):
    response = await client.get("/api/metrics")
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 0


async def test_metrics_aggregates_submissions(client, monkeypatch):
    async def analyze(_comment: str):
        return AIResult(
            sentiment="positive",
            request_category="collaboration",
            draft_reply="Thank you.",
        )

    monkeypatch.setattr("app.contact.service.analyze_comment", analyze)

    await client.post("/api/contact", json=VALID_PAYLOAD)
    await client.post("/api/contact", json=payload(email="other@example.com"))

    response = await client.get("/api/metrics?days=30")
    body = response.json()
    assert body["total"] == 2
    assert body["by_category"] == {"collaboration": 2}
    assert body["by_sentiment"] == {"positive": 2}
    assert body["ai_unavailable_count"] == 0


async def test_metrics_counts_ai_unavailable(client, monkeypatch):
    async def unavailable(_comment: str):
        return None

    monkeypatch.setattr("app.contact.service.analyze_comment", unavailable)

    await client.post("/api/contact", json=VALID_PAYLOAD)

    response = await client.get("/api/metrics?days=30")
    body = response.json()
    assert body["total"] == 1
    assert body["ai_unavailable_count"] == 1
