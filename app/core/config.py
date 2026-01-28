from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings): 
    DATABASE_URL: str = "sqlite+aiosqlite:///./fault_reports.db"
    model_config = SettingsConfigDict(env_file = ".env")

settings = Settings()