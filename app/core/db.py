from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.config import settings

"""classe base da cui erediteranno tutti i modelli"""
Base = declarative_base()

engine = create_async_engine(
    settings.DATABASE_URL, 
    echo = True, 
    connect_args={"check_same_thread": False}
)   

SessionLocal = async_sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
) 

async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
    