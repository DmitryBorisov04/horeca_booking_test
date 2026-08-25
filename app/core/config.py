from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "MISE Restaurant Booking API"

    DATABASE_URL: str = "sqlite+aiosqlite:///./bookings.db"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
