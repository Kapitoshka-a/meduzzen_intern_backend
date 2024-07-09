import pytest
from fastapi.testclient import TestClient
from app.db import async_session_maker
from app.services.user_crud import UserCRUD
from app.main import app

client = TestClient(app)


def test_get_users():
    response = client.get("/api/users")
    assert response.status_code == 200
    assert "users" in response.json()

    response = client.get("/api/users?skip=0&limit=2")
    assert response.status_code == 200
    assert len(response.json()["users"]) == 2


def test_add_user():
    user_data = {
        "email": "fish@example.com",
        "firstname": "fog",
        "lastname": "wet",
        "avatar": "test.png",
        "password1": "string123",
        "password2": "string123",
        "city": "Odes",
        "phone": "+380987654144"
    }
    response = client.post("/api/users/", json=user_data)
    assert response.status_code == 201


def test_get_user():
    response = client.get("/api/users/25")
    assert response.status_code == 200
    assert response.json()["id"] == 25

    response = client.get("/api/users/1")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_user():
    update_data = {
        "firstname": "test",
        "lastname": "test",
        "password": "secret_password",
        "avatar": "TestImage.png",
        "city": "Odes",
        "phone": "+380987654145"
    }
    async with async_session_maker() as session:
        user_crud = UserCRUD(session)
        user = await user_crud.get_user_by_email("fish@example.com")
        response = client.put(f"/api/users/{user.id}", json=update_data)
        assert response.status_code == 202
        assert response.json()["firstname"] == "test"

        response = client.put("/api/users/1", json=update_data)
        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"


@pytest.mark.asyncio
async def test_get_user_by_email():
    async with async_session_maker() as session:
        user_crud = UserCRUD(session)
        retrieved_user = await user_crud.get_user_by_email("fish@example.com")

        assert retrieved_user is not None
        assert retrieved_user.email == "fish@example.com"


@pytest.mark.asyncio
async def test_delete_user():
    async with async_session_maker() as session:
        user_crud = UserCRUD(session)
        user = await user_crud.get_user_by_email("fish@example.com")

        response = client.delete(f"/api/users/{user.id}")
        assert response.status_code == 204

        response = client.delete("/api/users/1")
        assert response.status_code == 404
