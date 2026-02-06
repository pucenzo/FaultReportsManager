from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.core.config import settings

"""mappa le classi python e le tabelle del db"""
Base = declarative_base()

"""creazione e configurazione del motore di connessione al db"""
engine = create_async_engine(
    settings.DATABASE_URL, 
    echo = True, 
    connect_args={"check_same_thread": False}
)   

"""creiamo un generatore di sessioni asincrone per ogni richiesta"""
SessionLocal = async_sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
) 