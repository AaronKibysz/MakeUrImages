"""Punto de entrada de la aplicacion FastAPI."""

from fastapi import FastAPI

from app.core.config import settings

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)


@app.get("/health", tags=["health"])
async def health() -> dict:
    return {"status": "ok"}