import pytest

from tests.helpers import VALID_PAYLOAD


@pytest.mark.parametrize("limit", [1, 2, 5], ids=["limit_1", "limit_2", "limit_5"])
async def test_rate_limit_allows_up_to_limit(client, monkeypatch, limit):
    monkeypatch.setattr("app.core.rate_limit.settings.rate_limit_requests", limit)

    for _ in range(limit):
        response = await client.post("/api/contact", json=VALID_PAYLOAD)
        assert response.status_code == 201


async def test_rate_limit_exceeded_on_limit_plus_one(client, monkeypatch):
    monkeypatch.setattr("app.core.rate_limit.settings.rate_limit_requests", 2)

    for _ in range(2):
        assert (await client.post("/api/contact", json=VALID_PAYLOAD)).status_code == 201

    response = await client.post("/api/contact", json=VALID_PAYLOAD)
    assert response.status_code == 429
    body = response.json()
    assert body["error"] == "rate_limit_exceeded"
    assert body["message"]
    assert response.headers.get("retry-after")
