from pydantic_settings import BaseSettings, SettingsConfigDict

"""
Centralizza tutte le configurazioni dell'applicazione:
1. url di connessione al db, con driver aiosqlite per i/o asincrono
2. comunica a Pydantic di caricare automaticamente le var. amb. dal file .env
3. durata del token JWT per l'autenticazione dell'utente
4. chiave crittografica privata per generazione token e verificare veridicità token
"""
class Settings(BaseSettings): 
    
    DATABASE_URL: str = "sqlite+aiosqlite:///./fault_reports.db"
    
    model_config = SettingsConfigDict(env_file = ".env")

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    SECRET_KEY: str

settings = Settings()