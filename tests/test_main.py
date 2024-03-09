
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app=app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Sigma API is up and running!"}
