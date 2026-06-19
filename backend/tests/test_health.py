async def test_health_smoke(client):
    response = await client.get("/api/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] in ("ok", "degraded")
    assert body["version"] == "1.0.0"
    assert "checks" in body
    assert "database" in body["checks"]
