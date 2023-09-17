from httpx import AsyncClient
import pytest


@pytest.mark.parametrize("email,password,status_code", [
    ("kot@pes.com", "kotopes", 200),
    ("kot@pes.com", "koto", 409),
    ("pes@kot.com", "kotopes", 200),
    ("peskot", "kotopes", 422),
])
async def test_register_user(ac: AsyncClient, email, password, status_code):
    response = await ac.post("/auth/register", json={
        "email": email,
        "password": password
    })
    assert response.status_code == status_code


@pytest.mark.parametrize("email,password,status_code", [
    ("test@test.com", "test", 200)
])
async def test_login_user(ac, email, password, status_code):
    response = await ac.post("/auth/login", json={
        "email": email,
        "password": password
    })
    assert response.status_code == status_code