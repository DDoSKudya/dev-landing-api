from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

PHONE_PATTERN = r"^\+?[0-9\s\-\(\)]{7,20}$"


class ContactCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    phone: str = Field(min_length=7, max_length=20, pattern=PHONE_PATTERN)
    email: EmailStr
    comment: str = Field(min_length=10, max_length=5000)

    @field_validator("name", "phone", "email", "comment", mode="before")
    @classmethod
    def strip_whitespace(cls, value: object) -> object:
        return value.strip() if isinstance(value, str) else value


class ContactResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    message: str
    ai_status: str
    sentiment: str | None
    request_category: str | None
    created_at: datetime
