from sqlalchemy import func, select

from app.contact.ai import AIResult
from app.contact.models import ContactSubmission
from app.core.database import async_session_factory
from app.core.exceptions import EmailDeliveryError
from tests.helpers import VALID_PAYLOAD


async def test_submit_persists_row_with_client_ip(client):
    response = await client.post("/api/contact", json=VALID_PAYLOAD)
    body = response.json()

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


async def test_submit_ai_unavailable_class(client, monkeypatch):
    async def unavailable(_comment: str):
        return None

    monkeypatch.setattr("app.contact.service.analyze_comment", unavailable)

    response = await client.post("/api/contact", json=VALID_PAYLOAD)
    assert response.status_code == 201
    body = response.json()
    assert body["ai_status"] == "unavailable"
    assert body["sentiment"] is None
    assert body["request_category"] is None


async def test_submit_ai_ok_class(client, monkeypatch):
    async def analyze(_comment: str):
        return AIResult(
            sentiment="positive",
            request_category="collaboration",
            draft_reply="Thank you for your interest.",
        )

    monkeypatch.setattr("app.contact.service.analyze_comment", analyze)

    response = await client.post("/api/contact", json=VALID_PAYLOAD)
    body = response.json()
    assert body["ai_status"] == "ok"
    assert body["sentiment"] == "positive"
    assert body["request_category"] == "collaboration"

    async with async_session_factory() as session:
        row = await session.scalar(
            select(ContactSubmission).where(ContactSubmission.id == body["id"])
        )

    assert row is not None
    assert row.ai_status == "ok"
    assert row.sentiment == "positive"
    assert row.request_category == "collaboration"
    assert row.ai_draft_reply == "Thank you for your interest."


async def test_submit_email_failure_still_persists_regression(client, monkeypatch):
    async def fail(*_args, **_kwargs):
        raise EmailDeliveryError()

    monkeypatch.setattr("app.contact.service.send_contact_emails", fail)

    response = await client.post("/api/contact", json=VALID_PAYLOAD)
    assert response.status_code == 502
    body = response.json()
    assert body["error"] == "email_delivery_failed"

    async with async_session_factory() as session:
        count = await session.scalar(select(func.count()).select_from(ContactSubmission))

    assert count == 1
