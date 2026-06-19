import logging
from email.message import EmailMessage
from pathlib import Path

import aiosmtplib
from jinja2 import Environment, FileSystemLoader, select_autoescape

from app.contact.models import ContactSubmission
from app.contact.schemas import ContactCreate
from app.core.config import settings
from app.core.exceptions import EmailDeliveryError

logger = logging.getLogger(__name__)

TEMPLATE_DIR = Path(__file__).resolve().parents[1] / "templates" / "email"
_jinja = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=select_autoescape(["html"]),
)


def _render_template(template_name: str, **context: object) -> str:
    return _jinja.get_template(template_name).render(**context)


async def _send_html_email(to: str, subject: str, html: str) -> None:
    message = EmailMessage()
    message["From"] = settings.email_from
    message["To"] = to
    message["Subject"] = subject
    message.set_content("Please view this email in an HTML-capable client.")
    message.add_alternative(html, subtype="html")

    await aiosmtplib.send(
        message,
        hostname=settings.smtp_host,
        port=settings.smtp_port,
        use_tls=settings.smtp_use_tls,
        username=settings.smtp_user or None,
        password=settings.smtp_password or None,
    )


async def send_contact_emails(data: ContactCreate, submission: ContactSubmission) -> None:
    try:
        owner_html = _render_template(
            "owner.html",
            name=data.name,
            phone=data.phone,
            email=data.email,
            comment=data.comment,
            sentiment=submission.sentiment,
            request_category=submission.request_category,
            draft_reply=submission.ai_draft_reply,
        )
        await _send_html_email(
            settings.email_owner,
            f"New contact from {data.name}",
            owner_html,
        )

        user_html = _render_template("user.html", name=data.name)
        await _send_html_email(
            data.email,
            "Мы получили ваше сообщение",
            user_html,
        )
    except Exception as exc:
        logger.warning("Email delivery failed", exc_info=True)
        raise EmailDeliveryError() from exc
