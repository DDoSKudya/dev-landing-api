from datetime import datetime

from sqlalchemy import select

from app.contact.models import ContactSubmission
from app.core.database import get_session


async def list_submissions_since(since: datetime) -> list[ContactSubmission]:
    session = get_session()
    result = await session.scalars(
        select(ContactSubmission)
        .where(ContactSubmission.created_at >= since)
        .order_by(ContactSubmission.created_at.desc())
    )
    return list(result.all())
