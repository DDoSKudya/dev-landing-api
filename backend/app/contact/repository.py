from uuid import uuid4

from app.contact.ai import AIResult
from app.contact.models import ContactSubmission
from app.contact.schemas import ContactCreate
from app.core.database import get_session


async def create_submission(
    data: ContactCreate,
    client_ip: str,
    ai_result: AIResult | None,
) -> ContactSubmission:
    submission = ContactSubmission(
        id=str(uuid4()),
        name=data.name,
        phone=data.phone,
        email=data.email,
        comment=data.comment,
        client_ip=client_ip,
        ai_status="ok" if ai_result else "unavailable",
        sentiment=ai_result.sentiment if ai_result else None,
        request_category=ai_result.request_category if ai_result else None,
        ai_draft_reply=ai_result.draft_reply if ai_result else None,
    )
    session = get_session()
    session.add(submission)
    await session.flush()
    await session.refresh(submission)
    return submission
