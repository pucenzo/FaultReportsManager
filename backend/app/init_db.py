from app.core.db import Base, engine, SessionLocal
import asyncio
from app.crud.crud_stato import get_stato_by_nome, create_stato
import app.models

"""Inizializza il database. Crea le tabelle se non esistono e popola la tabella StatoSegnalazione"""
async def init_db():

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with SessionLocal() as db: 
        lista_stati = ["Aperta", "In Lavorazione", "Risolta", "Chiusa"]

        for stato in lista_stati:
            stato_esiste = await get_stato_by_nome(db, stato)
            if not stato_esiste:
                await create_stato(db, stato)


        await db.commit()
        
if __name__ == "__main__":
    asyncio.run(init_db())