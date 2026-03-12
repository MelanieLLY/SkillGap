from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "postgresql://localhost/skillgap_db"
    secret_key: str = "secret"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    anthropic_api_key: str = ""

    model_config = SettingsConfigDict(
        env_file="server/.env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
