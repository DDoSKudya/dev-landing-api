from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.contact.schemas import ContactCreate, ContactResponse
from app.contact.service import submit_contact
from app.core.exceptions import EmailDeliveryError
from app.core.rate_limit import check_rate_limit

router = APIRouter(tags=["contact"])


def _client_ip(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


@router.post("/contact", status_code=201, response_model=ContactResponse)
async def post_contact(body: ContactCreate, request: Request) -> ContactResponse | JSONResponse:
    client_ip = _client_ip(request)
    check_rate_limit(client_ip)
    try:
        return await submit_contact(body, client_ip)
    except EmailDeliveryError as exc:
        return JSONResponse(
            status_code=502,
            content={"error": exc.code, "message": exc.message},
        )
