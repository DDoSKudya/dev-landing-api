import pytest

from tests.helpers import VALID_PAYLOAD, payload


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("name", "A"),
        ("name", "x" * 101),
        ("phone", "123456"),
        ("phone", "1" * 21),
        ("phone", "not-a-phone"),
        ("email", "not-an-email"),
        ("email", "missing-at.com"),
        ("comment", "x" * 9),
        ("comment", "x" * 5001),
    ],
    ids=[
        "name_len_Lmin-1",
        "name_len_Lmax+1",
        "phone_len_Lmin-1",
        "phone_len_Lmax+1",
        "phone_invalid_pattern",
        "email_invalid_format",
        "email_missing_at",
        "comment_len_Lmin-1",
        "comment_len_Lmax+1",
    ],
)
async def test_post_contact_invalid_field_class(client, field, value):
    response = await client.post("/api/contact", json=payload(**{field: value}))
    assert response.status_code == 422
    body = response.json()
    assert body["error"] == "validation_error"
    assert body["message"] == "Request validation failed"
    assert body["details"]


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("name", "Ab"),
        ("name", "x" * 100),
        ("phone", "1234567"),
        ("phone", "+7 (999) 123-45-67"),
        ("comment", "x" * 10),
        ("comment", "x" * 5000),
    ],
    ids=[
        "name_boundary_Lmin",
        "name_boundary_Lmax",
        "phone_boundary_Lmin",
        "phone_valid_formatted",
        "comment_boundary_Lmin",
        "comment_boundary_Lmax",
    ],
)
async def test_post_contact_valid_field_boundaries(client, field, value):
    response = await client.post("/api/contact", json=payload(**{field: value}))
    assert response.status_code == 201


@pytest.mark.parametrize(
    "missing_field",
    ["name", "phone", "email", "comment"],
    ids=lambda field: f"missing_{field}",
)
async def test_post_contact_missing_required_field(client, missing_field):
    body = payload()
    del body[missing_field]
    response = await client.post("/api/contact", json=body)
    assert response.status_code == 422
    assert response.json()["error"] == "validation_error"


async def test_post_contact_strips_whitespace(client):
    response = await client.post(
        "/api/contact",
        json={
            "name": "  Ivan Petrov  ",
            "phone": "  +79991234567  ",
            "email": "  ivan@example.com  ",
            "comment": "  Long enough comment.  ",
        },
    )
    assert response.status_code == 201


async def test_post_contact_happy_path_contract(client):
    response = await client.post("/api/contact", json=VALID_PAYLOAD)
    assert response.status_code == 201
    body = response.json()
    assert body["message"] == "Спасибо! Сообщение получено."
    assert body["ai_status"] in ("ok", "unavailable")
    assert "id" in body
    assert "created_at" in body
