from fastapi import APIRouter, Request

from app.contact.schemas import ContactCreate, ContactResponse
from app.contact.service import submit_contact

router = APIRouter(tags=["contact"])


def _client_ip(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


@router.post("/contact", status_code=201, response_model=ContactResponse)
async def post_contact(body: ContactCreate, request: Request) -> ContactResponse:
    return await submit_contact(body, _client_ip(request))
