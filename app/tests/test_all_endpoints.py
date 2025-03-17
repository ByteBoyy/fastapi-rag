
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Store tokens
tokens = {}

@pytest.mark.run(order=1)
def test_set_admin_role_directly():
    from app.database import users_collection
    users_collection.update_one({"username": "adminuser"}, {"$set": {"role": "admin"}})

def test_register_user():
    response = client.post("/users/register", json={
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpass"
    })
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_register_admin():
    response = client.post("/users/register", json={
        "username": "adminuser",
        "email": "admin@example.com",
        "password": "adminpass"
    })
    assert response.status_code == 200
    assert response.json()["username"] == "adminuser"

def test_login_user():
    response = client.post("/users/login", json={
        "username": "testuser",
        "password": "testpass"
    })
    assert response.status_code == 200
    tokens["user"] = response.json()["access_token"]

def test_login_admin():
    response = client.post("/users/login", json={
        "username": "adminuser",
        "password": "adminpass"
    })
    assert response.status_code == 200
    tokens["admin"] = response.json()["access_token"]

def test_read_profile_user():
    headers = {"Authorization": f"Bearer {tokens['user']}"}
    response = client.get("/users/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_read_profile_admin():
    headers = {"Authorization": f"Bearer {tokens['admin']}"}
    response = client.get("/users/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["username"] == "adminuser"

def test_upload_pdf_user_forbidden():
    headers = {"Authorization": f"Bearer {tokens['user']}"}
    with open("sample.pdf", "wb") as f:
        f.write(b"Dummy PDF content for testing.")
    with open("sample.pdf", "rb") as pdf:
        response = client.post("/rag/upload", files={"file": pdf}, headers=headers)
    assert response.status_code == 403


def test_query_rag_user_allowed():
    headers = {"Authorization": f"Bearer {tokens['user']}"}
    response = client.get("/rag/query", params={"question": "What is this?"}, headers=headers)
    assert response.status_code == 200
    assert "answer" in response.json()

def test_query_rag_admin_allowed():
    headers = {"Authorization": f"Bearer {tokens['admin']}"}
    response = client.get("/rag/query", params={"question": "Tell me something"}, headers=headers)
    assert response.status_code == 200
    assert "answer" in response.json()

def test_delete_user_by_user_forbidden():
    headers = {"Authorization": f"Bearer {tokens['user']}"}
    response = client.delete("/users/delete", params={"username": "adminuser"}, headers=headers)
    assert response.status_code == 403


