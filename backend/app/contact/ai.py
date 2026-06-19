import json
import logging

from openai import AsyncOpenAI
from pydantic import BaseModel, ValidationError

from app.core.config import settings

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "Analyze the contact form comment. Reply with JSON only using this shape: "
    '{"sentiment": "positive|neutral|negative", '
    '"request_category": "collaboration|question|feedback|other", '
    '"draft_reply": "2-4 sentences in the same language as the comment"}. '
    "Do not promise specific deadlines in draft_reply."
)


class AIResult(BaseModel):
    sentiment: str
    request_category: str
    draft_reply: str


async def analyze_comment(comment: str) -> AIResult | None:
    if not settings.openai_api_key:
        return None

    try:
        client = AsyncOpenAI(
            api_key=settings.openai_api_key,
            timeout=settings.openai_timeout_sec,
        )
        response = await client.chat.completions.create(
            model=settings.openai_model,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": comment},
            ],
        )
        content = response.choices[0].message.content
        if not content:
            return None
        return AIResult.model_validate(json.loads(content))
    except (ValidationError, json.JSONDecodeError, Exception):
        logger.warning("AI unavailable", exc_info=True)
        return None
