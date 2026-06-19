from sqlalchemy import select

from app.contact.models import ContactSubmission
from app.core.database import async_session_factory

VALID_PAYLOAD = {
    "name": "Ivan Petrov",
    "phone": "+79991234567",
    "email": "ivan@example.com",
    "comment": "Interested in collaboration on FastAPI.",
}


async def test_post_contact_success(client):
    response = await client.post("/api/contact", json=VALID_PAYLOAD)
    assert response.status_code == 201
    body = response.json()
    assert body["message"] == "Thank you! Your message was received."
    assert body["ai_status"] == "unavailable"
    assert body["sentiment"] is None
    assert body["request_category"] is None
    assert "id" in body
    assert "created_at" in body

    async with async_session_factory() as session:
        row = await session.scalar(
            select(ContactSubmission).where(ContactSubmission.id == body["id"])
        )

    assert row is not None
    assert row.name == VALID_PAYLOAD["name"]
    assert row.phone == VALID_PAYLOAD["phone"]
    assert row.email == VALID_PAYLOAD["email"]
    assert row.comment == VALID_PAYLOAD["comment"]
    assert row.client_ip == "127.0.0.1"


async def test_post_contact_invalid_email(client):
    response = await client.post(
        "/api/contact",
        json={**VALID_PAYLOAD, "email": "not-an-email"},
    )
    assert response.status_code == 422
    body = response.json()
    assert body["error"] == "validation_error"
