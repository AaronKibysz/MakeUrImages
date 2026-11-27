"""Tests unitarios minimos para el endpoint /health y la configuracion."""

import os

# Valores por defecto para permitir instanciar settings sin .env en CI.
os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://user:pass@localhost:5432/makeurimages")
os.environ.setdefault("JWT_SECRET", "test-secret-for-tests")

from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app


def test_health_returns_200_and_ok() -> None:
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_config_loads_defaults() -> None:
    assert settings.APP_NAME == "MakeUrImages"
    assert settings.AI_PROVIDER == "mock"