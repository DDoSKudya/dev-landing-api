from app.contact.ai import AIResult

VALID_PAYLOAD = {
    "name": "Ivan Petrov",
    "phone": "+79991234567",
    "email": "ivan@example.com",
    "comment": "Interested in collaboration on FastAPI.",
}


async def test_metrics_empty(client):
    response = await client.get("/api/metrics?days=30")
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 0
    assert body["by_category"] == {}
    assert body["by_sentiment"] == {}
    assert body["ai_unavailable_count"] == 0


async def test_metrics_after_submissions(client, monkeypatch):
    async def analyze(_comment: str):
        return AIResult(
            sentiment="positive",
            request_category="collaboration",
            draft_reply="Thank you.",
        )

    monkeypatch.setattr("app.contact.service.analyze_comment", analyze)

    await client.post("/api/contact", json=VALID_PAYLOAD)
    await client.post(
        "/api/contact",
        json={**VALID_PAYLOAD, "email": "other@example.com"},
    )

    response = await client.get("/api/metrics?days=30")
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 2
    assert body["by_category"] == {"collaboration": 2}
    assert body["by_sentiment"] == {"positive": 2}
    assert body["ai_unavailable_count"] == 0


async def test_metrics_invalid_days(client):
    response = await client.get("/api/metrics?days=0")
    assert response.status_code == 422
