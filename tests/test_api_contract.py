from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


def test_openapi_schema_generated():
    response = client.get("/api/v1/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert data["info"]["title"] == "Comic & Manga Inventory API"
    assert "/api/v1/products/" in data["paths"]
    assert "/api/v1/products/low-stock" in data["paths"]
    assert "/api/v1/auth/login" in data["paths"]


def test_products_contract_mock():
    response = client.get("/api/v1/products/")
    assert response.status_code == 200
    products = response.json()
    assert isinstance(products, list)
    assert len(products) > 0
    assert "titulo_nombre" in products[0]
    assert "precio_venta" in products[0]


def test_low_stock_contract_mock():
    response = client.get("/api/v1/products/low-stock?threshold=3")
    assert response.status_code == 200
    alerts = response.json()
    assert isinstance(alerts, list)
    assert len(alerts) > 0
    assert "producto" in alerts[0]
    assert "stock_minimo_umbral" in alerts[0]
