"""Tests for QueueLens API endpoints. Run with: pytest"""
import sys
from pathlib import Path
import pytest

# Ensure project root is in sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app import app


@pytest.fixture()
def client():
    app.config.update(TESTING=True)
    with app.test_client() as test_client:
        yield test_client


def test_home_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"QueueLens" in response.data


def test_health_endpoint(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["status"] == "healthy"
    assert payload["model_loaded"] is True
    assert "threshold" in payload


def test_options_endpoint(client):
    response = client.get("/api/options")
    assert response.status_code == 200
    payload = response.get_json()
    assert "options" in payload
    for key in ["agency", "complaint_type", "borough"]:
        assert key in payload["options"]
        assert len(payload["options"][key]) > 0


def test_predict_rejects_missing_fields(client):
    response = client.post("/api/predict", json={})
    assert response.status_code == 400
    assert "missing_fields" in response.get_json()


def test_predict_rejects_invalid_hour(client):
    response = client.post(
        "/api/predict",
        json={
            "agency": "DEP",
            "complaint_type": "Air Quality",
            "borough": "MANHATTAN",
            "created_hour": 99,
            "created_day": 15,
            "created_month": 6,
        },
    )
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_predict_valid_request(client):
    response = client.post(
        "/api/predict",
        json={
            "agency": "DEP",
            "complaint_type": "Air Quality",
            "borough": "MANHATTAN",
            "created_hour": 12,
            "created_day": 15,
            "created_month": 6,
        },
    )
    assert response.status_code == 200
    payload = response.get_json()
    assert "probability" in payload
    assert "probability_percent" in payload
    assert "risk_level" in payload
    assert payload["risk_level"] in ["High", "Lower"]
    assert "prediction" in payload
    assert "threshold" in payload


def test_predict_supports_created_hours_alias(client):
    response = client.post(
        "/api/predict",
        json={
            "agency": "DEP",
            "complaint_type": "Air Quality",
            "borough": "MANHATTAN",
            "created_hours": 12,
            "created_day": 15,
            "created_month": 6,
        },
    )
    assert response.status_code == 200
    payload = response.get_json()
    assert "probability" in payload
    assert "risk_level" in payload
