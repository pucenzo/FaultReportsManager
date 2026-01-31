from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import LogStatoSegnalazione

async def create_log(
    db: AsyncSession, 
    id_segnalazione: int,
    vecchio_stato: str|None,
    nuovo_stato: str
) -> LogStatoSegnalazione:
    
    db_log = LogStatoSegnalazione(
        vecchio_stato = vecchio_stato, 
        nuovo_stato = nuovo_stato, 
        id_segnalazione = id_segnalazione
    )
    
    db.add(db_log)
    await db.commit()
    await db.refresh(db_log)
    return db_log


async def get_log_by_segnalazione(
    db: AsyncSession, 
    id_segnalazione: int
) -> list[LogStatoSegnalazione]:
    
    query = (select(LogStatoSegnalazione)
            .where(LogStatoSegnalazione.id_segnalazione == id_segnalazione)
            .order_by(LogStatoSegnalazione.data_modifica.asc())
    )
    result = await db.execute(query)
    return result.scalars().all()