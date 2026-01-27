from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.config import settings

engine = create_async_engine(settings.DATABASE_URL,connect_args={"check_same_thread": False})   

SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine) 

async def get_db():
    async with SessionLocal() as session:
        yield session