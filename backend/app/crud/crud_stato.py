from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import StatoSegnalazione

"""
Permette la creazione degli stati nel db. 
Utile per l'inizializzazione della tabella StatiSegnalazione
"""
async def create_stato(
    db: AsyncSession,
    nome: str
) -> StatoSegnalazione:
    
    db_stato = StatoSegnalazione(nome = nome)
    db.add(db_stato)
    await db.commit()
    await db.refresh(db_stato)
    return db_stato

"""Recupera lo stato tramite il suo nome"""
async def get_stato_by_nome(
    db: AsyncSession, 
    nome: str
) -> StatoSegnalazione:
    
    query = select(StatoSegnalazione).where(StatoSegnalazione.nome == nome)
    result = await db.execute(query)
    return result.scalar_one_or_none()

"""Recupera tutti gli stati presenti nel db"""
async def get_stati(
    db: AsyncSession
) -> list[StatoSegnalazione]:
    
    query = select(StatoSegnalazione)
    result = await db.execute(query)
    return result.scalars().all()