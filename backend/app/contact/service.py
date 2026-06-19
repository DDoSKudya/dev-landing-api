from app.contact import repository
from app.contact.ai import analyze_comment
from app.contact.email import send_contact_emails
from app.contact.schemas import ContactCreate, ContactResponse

SUCCESS_MESSAGE = "Thank you! Your message was received."


async def submit_contact(data: ContactCreate, client_ip: str) -> ContactResponse:
    ai_result = await analyze_comment(data.comment)
    submission = await repository.create_submission(data, client_ip, ai_result)
    await send_contact_emails(data, submission)
    return ContactResponse(
        id=submission.id,
        message=SUCCESS_MESSAGE,
        ai_status=submission.ai_status,
        sentiment=submission.sentiment,
        request_category=submission.request_category,
        created_at=submission.created_at,
    )
