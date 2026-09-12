"""Application configuration loaded from environment variables.

This file reads from the .env file and creates a `settings` object
that you can import anywhere in the app to get config values.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """All app settings come from .env file or environment variables."""
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Database
    database_url: str

    # JWT Auth
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # AWS S3
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_bucket_name: str
    aws_region: str

    # Stripe
    stripe_secret_key: str = "sk_test_placeholder"
    stripe_webhook_secret: str = "whsec_placeholder"

    # App
    app_name: str = "Digital Market"
    debug: bool = True


# Create a single settings instance that the whole app uses
settings = Settings()