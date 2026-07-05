"""Application settings and configuration."""

from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration settings."""

    # Project
    version: str = "1.0.0"
    environment: str = "development"

    # Discord
    discord_token: str
    discord_guild_id: Optional[int] = None
    bot_prefix: str = "!"

    # Warcraft Logs
    warcraft_logs_client_id: str
    warcraft_logs_client_secret: str
    warcraft_logs_redirect_uri: str = "http://localhost:8000/callback"

    # Battle.net
    battlenet_api_key: str
    battlenet_region: str = "us"

    # Database
    database_url: str = "sqlite:///./logrun.db"

    # Bot Settings
    log_level: str = "INFO"
    refresh_interval: int = 3600  # seconds
    cache_ttl: int = 1800  # seconds

    # API
    keep_alive_port: int = 8000
    keep_alive_host: str = "0.0.0.0"

    class Config:
        """Pydantic config."""
        env_file = ".env"
        case_sensitive = False


settings = Settings()
