from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from typing import Optional

from app.schemas import SegnalazioneCreate, SegnalazioneUpdatePriorita, SegnalazioneUpdateStato
from app.models import Segnalazione, StatoSegnalazione, LogStatoSegnalazione, Messaggio
from app.models import Priorita

"""
Crea la segnalazione. 
Utilizza lo schema SegnalazioneCreate per la validazione dei dati in input.
Genera il primo messaggio della chat
"""
async def create_segnalazione(
    db: AsyncSession,
    segnalazione_in: SegnalazioneCreate,
    id_cliente: int,
    id_stato_iniziale: int,
    autore: str
) -> Segnalazione:
    
    db_segnalazione = Segnalazione(
        titolo = segnalazione_in.titolo,
        descrizione = segnalazione_in.descrizione,
        id_cliente = id_cliente,
        id_stato = id_stato_iniziale
    )

    db.add(db_segnalazione)
    await db.flush()

    primo_messaggio = Messaggio(
        id_segnalazione = db_segnalazione.id,
        contenuto = segnalazione_in.descrizione,
        autore = autore, 
        ruolo = "Cliente"
    )

    db.add(primo_messaggio)

    await db.commit()
    await db.refresh(db_segnalazione)

    query = (
        select(Segnalazione)
        .where(Segnalazione.id == db_segnalazione.id)
        .options(
            selectinload(Segnalazione.cliente),
            selectinload(Segnalazione.stato),
            selectinload(Segnalazione.messaggi)
        )
    )
    result = await db.execute(query)
    segnalazione_completa = result.scalar_one()
    return segnalazione_completa

"""
Recupera la lista delle segnalazioni.
Verifica la presenza di filtri per stato o priorità
"""
async def get_segnalazioni(
    db: AsyncSession, 
    priorita: Optional[Priorita] = None,
    id_stato: Optional[int] = None
) -> list[Segnalazione]|None:
    
    query = (select(Segnalazione)
            .options(
                selectinload(Segnalazione.cliente),
                selectinload(Segnalazione.stato), 
            )
    )

    if id_stato is not None:
        query = query.where(Segnalazione.id_stato == id_stato)
    
    if priorita is not None:
        query = query.where(Segnalazione.priorita == priorita)

    result = await db.execute(query)
    return result.scalars().all()

"""
Recupera le segnalazioni dell'utente.
Verifica la presenza dei filtri per stato o priorità
"""
async def get_segnalazione_by_cliente(
    db: AsyncSession,
    id_stato: int,
    priorita: Priorita,
    id_cliente: int
) -> list[Segnalazione]|None:
    
    query = (select(Segnalazione)
            .where(Segnalazione.id_cliente == id_cliente)
            .options(
                selectinload(Segnalazione.cliente),
                selectinload(Segnalazione.stato), 
            )
    )

    if id_stato is not None:
        query = query.where(Segnalazione.id_stato == id_stato)
    
    if priorita is not None:
        query = query.where(Segnalazione.priorita == priorita)
    
    result = await db.execute(query)
    return result.scalars().all()

"""
Recupera una determinata segnalazione tramite id. 
Utilizzata per leggerne i dettagli e la chat con l'operatore
"""    
async def get_segnalazione_by_id(
    db: AsyncSession,
    id_segnalazione: int
) -> Segnalazione|None:
    
    query = (select(Segnalazione)
            .where(Segnalazione.id == id_segnalazione)
            .options(
                selectinload(Segnalazione.cliente),
                selectinload(Segnalazione.stato), 
                selectinload(Segnalazione.messaggi)
            )
    )
    result = await db.execute(query)
    return result.scalar_one_or_none()

"""
Consente all'operatore di aggiornare lo stato di una segnalazione.
Gestisce la generazione del log di cambio stato (se lo stato è diverso da quello prec.).
Gestisce la generazione del messaggio di cambio stato.
"""
async def update_stato_segnalazione(
    db: AsyncSession,
    id_segnalazione: int,
    nuovo_stato: SegnalazioneUpdateStato,
    operatore: str
) -> Segnalazione|None:
    
    query = (select(Segnalazione)
                .where(Segnalazione.id == id_segnalazione)
                .options(
                    selectinload(Segnalazione.cliente),
                    selectinload(Segnalazione.stato), 
                    selectinload(Segnalazione.messaggi)
                )
            )
    
    result = await db.execute(query)
    segnalazione_da_aggiornare = result.scalar_one_or_none()

    if segnalazione_da_aggiornare is None:
        return None
    
    vecchio_stato = segnalazione_da_aggiornare.stato.nome
    
    query_nuovo_stato = (select(StatoSegnalazione).where(StatoSegnalazione.id == nuovo_stato.id_stato))
    result_query_nuovo_stato = await db.execute(query_nuovo_stato)
    nuovo_stato_obj = result_query_nuovo_stato.scalar_one_or_none()

    if not nuovo_stato_obj:
        return None
    
    nome_nuovo_stato = nuovo_stato_obj.nome

    if segnalazione_da_aggiornare.id_stato != nuovo_stato.id_stato:
        db_log = LogStatoSegnalazione(
            vecchio_stato = vecchio_stato,
            nuovo_stato = nome_nuovo_stato,
            id_segnalazione = id_segnalazione,
            operatore = operatore
        )

        db.add(db_log)

        messaggio_aggiornamento = Messaggio(
            id_segnalazione = id_segnalazione,
            contenuto = f"Lo stato è stato aggiornato da {vecchio_stato} a {nome_nuovo_stato}",
            autore = operatore,
            ruolo = "operatore"
        )

        db.add(messaggio_aggiornamento)

    segnalazione_da_aggiornare.id_stato = nuovo_stato.id_stato

    await db.commit()
    await db.refresh(segnalazione_da_aggiornare)
    return segnalazione_da_aggiornare

"""
Consente all'operatore di aggiornare la priorità di una segnalazione.
Gestisce la generazione del messaggio di cambio priorità (se la nuova è diversa da quella prec.).
"""
async def update_priorita_segnalazione(
    db: AsyncSession, 
    id_segnalazione: int,
    nuova_priorita: SegnalazioneUpdatePriorita,
    operatore: str
) -> Segnalazione|None:
    
    query = (select(Segnalazione)
                .where(Segnalazione.id == id_segnalazione)
                .options(
                    selectinload(Segnalazione.cliente),
                    selectinload(Segnalazione.stato), 
                    selectinload(Segnalazione.messaggi)
                )        
            )
    
    result = await db.execute(query)
    segnalazione_da_aggiornare = result.scalar_one_or_none()

    if segnalazione_da_aggiornare is None:
        return None
    
    vecchia_priorita = segnalazione_da_aggiornare.priorita

    if vecchia_priorita != nuova_priorita.priorita:
        messaggio_aggiornamento = Messaggio(
            id_segnalazione = id_segnalazione,
            contenuto = f"La priorità è stata aggiornata da {vecchia_priorita.value} a {nuova_priorita.priorita.value}",
            autore = operatore,
            ruolo = "operatore"
        )

        db.add(messaggio_aggiornamento)

    segnalazione_da_aggiornare.priorita = nuova_priorita.priorita

    await db.commit()
    await db.refresh(segnalazione_da_aggiornare)
    return segnalazione_da_aggiornare

"""
Crea un nuovo messaggio.
Se è il primo messaggio dell'operatore in risposta ad una segnalazione, 
aggiorna l'operatore che l'ha presa in carico
"""
async def create_messaggio(
    db: AsyncSession, 
    id_segnalazione: int,
    contenuto: str,
    autore: str, 
    ruolo: str
) -> Messaggio:
    
    nuovo_messaggio = Messaggio(
        contenuto = contenuto, 
        autore = autore,
        ruolo = ruolo, 
        id_segnalazione = id_segnalazione
    )

    if ruolo == "operatore":
        query = (update(Segnalazione)
                .where(Segnalazione.id == id_segnalazione)
                .where(Segnalazione.operatore.is_(None))
                .values(operatore=autore)
        )
        await db.execute(query)

    db.add(nuovo_messaggio)
    await db.commit()
    await db.refresh(nuovo_messaggio)
    return nuovo_messaggio

"""recupera il log della segnalazione"""

async def get_logs_by_segnalazione(
    db: AsyncSession,
    id_segnalazione: int
) -> list[LogStatoSegnalazione]:
    
    query = select(LogStatoSegnalazione).where(LogStatoSegnalazione.id_segnalazione == id_segnalazione)
    result = await db.execute(query)
    return result.scalars().all()    