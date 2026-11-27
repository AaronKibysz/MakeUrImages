"""Configuracion de la aplicacion via variables de entorno."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    APP_NAME: str = "MakeUrImages"
    APP_ENV: str = "development"
    DEBUG: bool = False
    REGION: str = "sa-east-1"

    DATABASE_URL: str  # Requerido. Sin valor por defecto para evitar credenciales en código.

    SUPABASE_URL: str = ""
    SUPABASE_ANON_KEY: str = ""
    SUPABASE_SERVICE_ROLE_KEY: str = ""

    R2_ACCOUNT_ID: str = ""
    R2_ACCESS_KEY_ID: str = ""
    R2_SECRET_ACCESS_KEY: str = ""
    R2_BUCKET_NAME: str = ""
    R2_ENDPOINT_URL: str = ""

    JWT_SECRET: str  # Requerido. Sin valor por defecto para evitar secreto débil en código.
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60

    AI_PROVIDER: str = "mock"
    AI_API_KEY: str = ""

    REDIS_URL: str = "redis://localhost:6379/0"


settings = Settings()