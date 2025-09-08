from fastapi.testclient import TestClient
from app.main import app
from app import utils

client = TestClient(app)

def test_root():
    r = client.get("/")
    assert r.status_code == 200

def test_utils_bad_smell():
    assert utils.bad_smell(1) == 1 + 3.14
