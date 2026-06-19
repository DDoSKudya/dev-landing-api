from datetime import datetime

from sqlalchemy import DateTime, Index, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class ContactSubmission(Base):
    __tablename__ = "contact_submissions"
    __table_args__ = (Index("ix_contact_submissions_created_at", "created_at"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    phone: Mapped[str] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(String(255))
    comment: Mapped[str] = mapped_column(Text)
    client_ip: Mapped[str] = mapped_column(String(45))
    sentiment: Mapped[str | None] = mapped_column(String(20), nullable=True)
    request_category: Mapped[str | None] = mapped_column(String(50), nullable=True)
    ai_draft_reply: Mapped[str | None] = mapped_column(Text, nullable=True)
    ai_status: Mapped[str] = mapped_column(String(20), default="unavailable")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
