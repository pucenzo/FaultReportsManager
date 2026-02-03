from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import Optional

from app.schemas import SegnalazioneCreate, SegnalazioneUpdatePriorita, SegnalazioneUpdateStato, SegnalazioneResponse
from app.models import Segnalazione, StatoSegnalazione, LogStatoSegnalazione
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

    query = (
        select(Segnalazione)
        .where(Segnalazione.id == db_segnalazione.id)
        .options(
            selectinload(Segnalazione.cliente),
            selectinload(Segnalazione.stato)
        )
    )
    result = await db.execute(query)
    segnalazione_completa = result.scalar_one()
    return segnalazione_completa

async def get_segnalazioni(
    db: AsyncSession, 
    priorita: Optional[Priorita] = None,
    id_stato: Optional[int] = None
) -> list[Segnalazione]|None:
    
    query = (select(Segnalazione)
            .options(
                selectinload(Segnalazione.cliente),
                selectinload(Segnalazione.stato)
            )
    )

    if id_stato is not None:
        query = query.where(Segnalazione.id_stato == id_stato)
    
    if priorita is not None:
        query = query.where(Segnalazione.priorita == priorita)

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

async def update_stato_segnalazione(
    db: AsyncSession,
    id_segnalazione: int,
    nuovo_stato: SegnalazioneUpdateStato
) -> Segnalazione|None:
    
    query = (select(Segnalazione)
                .where(Segnalazione.id == id_segnalazione)
                .options(
                    selectinload(Segnalazione.cliente),
                    selectinload(Segnalazione.stato)
                )
            )
    
    result = await db.execute(query)
    segnalazione_da_aggiornare = result.scalar_one_or_none()

    if segnalazione_da_aggiornare is None:
        return None
    
    vecchio_stato = segnalazione_da_aggiornare.stato.nome
    
    query_nuovo_stato = select(StatoSegnalazione).where(StatoSegnalazione.id == nuovo_stato.id_stato)
    result_query_nuovo_stato = await db.execute(query_nuovo_stato)
    nuovo_stato_obj = result_query_nuovo_stato.scalar_one_or_none()

    if not nuovo_stato_obj:
        return None
    
    nome_nuovo_stato = nuovo_stato_obj.nome

    if segnalazione_da_aggiornare.id_stato != nuovo_stato.id_stato:
        db_log = LogStatoSegnalazione(
            vecchio_stato = vecchio_stato,
            nuovo_stato = nome_nuovo_stato,
            id_segnalazione = id_segnalazione
        )

        db.add(db_log)

    segnalazione_da_aggiornare.id_stato = nuovo_stato.id_stato

    await db.commit()
    await db.refresh(segnalazione_da_aggiornare)
    return segnalazione_da_aggiornare

async def update_priorita_segnalazione(
    db: AsyncSession, 
    id_segnalazione: int,
    nuova_priorita: SegnalazioneUpdatePriorita
) -> Segnalazione|None:
    
    query = (select(Segnalazione)
                .where(Segnalazione.id == id_segnalazione)
                .options(
                    selectinload(Segnalazione.cliente),
                    selectinload(Segnalazione.stato)
                )        
            )
    
    result = await db.execute(query)
    segnalazione_da_aggiornare = result.scalar_one_or_none()

    if segnalazione_da_aggiornare is None:
        return None

    segnalazione_da_aggiornare.priorita = nuova_priorita.priorita

    await db.commit()
    await db.refresh(segnalazione_da_aggiornare)
    return segnalazione_da_aggiornare