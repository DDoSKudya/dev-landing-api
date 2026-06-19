VALID_PAYLOAD = {
    "name": "Ivan Petrov",
    "phone": "+79991234567",
    "email": "ivan@example.com",
    "comment": "Interested in collaboration on FastAPI.",
}


def payload(**overrides: object) -> dict:
    return {**VALID_PAYLOAD, **overrides}
