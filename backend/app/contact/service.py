from app.contact import repository
from app.contact.schemas import ContactCreate, ContactResponse

SUCCESS_MESSAGE = "Thank you! Your message was received."


async def submit_contact(data: ContactCreate, client_ip: str) -> ContactResponse:
    submission = await repository.create_submission(data, client_ip)
    return ContactResponse(
        id=submission.id,
        message=SUCCESS_MESSAGE,
        ai_status=submission.ai_status,
        sentiment=submission.sentiment,
        request_category=submission.request_category,
        created_at=submission.created_at,
    )
