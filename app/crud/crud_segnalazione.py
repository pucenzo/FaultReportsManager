from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.schemas import SegnalazioneCreate, SegnalazioneUpdatePriorita, SegnalazioneUpdateStato, SegnalazioneResponse
from app.models import Segnalazione
from app.models import Priorita

async def create_segnalazione(
    db: AsyncSession, 
    segnalazione_in: SegnalazioneCreate,
    id_cliente: int,
    id_stato_iniziale: int
) -> Segnalazione:
    
    db_segnalazione = Segnalazione(
        titolo = segnalazione_in.titolo,
        descrizione = segnalazione_in.descrizione,
        id_cliente = id_cliente,
        id_stato = id_stato_iniziale
    )

    db.add(db_segnalazione)
    await db.commit()
    await db.refresh(db_segnalazione)
    return db_segnalazione

async def get_segnalazioni(
        db:AsyncSession,
) -> list[Segnalazione]:
    
    query = (select(Segnalazione)
            .options(
                selectinload(Segnalazione.cliente),
                selectinload(Segnalazione.stato)
            )       
    )
    result = await db.execute(query)
    return result.scalars().all()

async def get_segnalazione_by_cliente(
    db: AsyncSession,
    id_cliente: int
) -> list[Segnalazione]|None:
    
    query = (select(Segnalazione)
            .where(Segnalazione.id_cliente == id_cliente)
            .options(
                selectinload(Segnalazione.cliente),
                selectinload(Segnalazione.stato)
            )
    )
    result = await db.execute(query)
    return result.scalars().all()
    
async def get_segnalazione_by_id(
    db: AsyncSession,
    id_segnalazione: int
) -> Segnalazione|None:
    
    query = (select(Segnalazione)
            .where(Segnalazione.id == id_segnalazione)
            .options(
                selectinload(Segnalazione.cliente),
                selectinload(Segnalazione.stato)
            )
    )
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def get_segnalazione_by_priorita(
    db: AsyncSession, 
    priorita: Priorita
) -> list[Segnalazione]|None:
    
    query = (select(Segnalazione)
            .where(Segnalazione.priorita == priorita)
            .options(
                selectinload(Segnalazione.cliente),
                selectinload(Segnalazione.stato)
            )
    )
    result = await db.execute(query)
    return result.scalars().all()
    
async def get_segnalazione_by_stato(
    db: AsyncSession, 
    id_stato: int
) -> list[Segnalazione]|None:
    
    query = (select(Segnalazione)
            .where(Segnalazione.id_stato == id_stato)
            .options(
                selectinload(Segnalazione.cliente),
                selectinload(Segnalazione.stato)
            )
    )                    
    result = await db.execute(query)
    return result.scalars().all()