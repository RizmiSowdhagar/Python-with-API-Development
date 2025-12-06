from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_reports_summary_endpoint_works():
    response = client.get("/reports/summary")
    assert response.status_code == 200

    data = response.json()
    # Basic shape checks
    assert "total_calculations" in data
    assert "per_operation" in data
    assert "last_calculation_at" in data
    assert isinstance(data["per_operation"], list)
