"""
This file was created by ]init[ AG 2023.

Module for testing REST service endpoint "/health".
"""
from ai_development.data_model import HealthCheck
from ai_development.service import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_health():
    """
    Test the health FastAPI endpoint.
    """
    response = client.get("/health")
    assert response.status_code == 200

    # Validate the response matches the HealthCheck schema
    health_check = HealthCheck(**response.json())
    assert health_check.status == "OK"
