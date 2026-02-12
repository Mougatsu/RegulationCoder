"""Configuration management using Pydantic Settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Anthropic API
    anthropic_api_key: str = ""
    extraction_model: str = "claude-sonnet-4-5-20250929"
    judge_model: str = "claude-opus-4-6"

    # Database
    database_url: str = "postgresql+asyncpg://regulationcoder:regulationcoder@localhost:5432/regulationcoder"

    # Logging & Audit
    log_level: str = "INFO"
    audit_log_dir: str = "./audit_logs"

    # Pipeline
    max_judge_retries: int = 2
    judge_timeout: int = 120
    batch_size: int = 5


def get_settings() -> Settings:
    """Get application settings (cached)."""
    return Settings()
