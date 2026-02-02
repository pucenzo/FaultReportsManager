from app.core.db import SessionLocal

async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()