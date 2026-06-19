from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parents[2]
PROJECT_ROOT = BACKEND_DIR.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Dev Landing API"
    debug: bool = False
    log_level: str = "INFO"

    cors_origins: str = "http://localhost:5173,http://localhost"

    data_dir: Path | None = None
    logs_dir: Path | None = None

    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    openai_timeout_sec: int = 15

    smtp_host: str = "localhost"
    smtp_port: int = 1025
    smtp_user: str = ""
    smtp_password: str = ""
    smtp_use_tls: bool = False
    email_from: str = "noreply@example.com"
    email_owner: str = "owner@example.com"

    rate_limit_requests: int = 5
    rate_limit_window_sec: int = 3600

    @property
    def resolved_data_dir(self) -> Path:
        return self.data_dir or (PROJECT_ROOT / "data")

    @property
    def resolved_logs_dir(self) -> Path:
        return self.logs_dir or (PROJECT_ROOT / "logs")

    @property
    def database_url(self) -> str:
        return f"sqlite+aiosqlite:///{self.resolved_data_dir / "app.db"}"

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


settings = Settings()
