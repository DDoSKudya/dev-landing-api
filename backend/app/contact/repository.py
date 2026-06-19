from uuid import uuid4

from app.contact.models import ContactSubmission
from app.contact.schemas import ContactCreate
from app.core.database import get_session


async def create_submission(data: ContactCreate, client_ip: str) -> ContactSubmission:
    submission = ContactSubmission(
        id=str(uuid4()),
        name=data.name,
        phone=data.phone,
        email=data.email,
        comment=data.comment,
        client_ip=client_ip,
        ai_status="unavailable",
    )
    session = get_session()
    session.add(submission)
    await session.flush()
    await session.refresh(submission)
    return submission
