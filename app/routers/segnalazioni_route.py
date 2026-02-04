from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.schemas import LogStatoSegnalazioneResponse, SegnalazioneCreate, SegnalazioneMinimal, SegnalazioneDetail, SegnalazioneUpdateStato, SegnalazioneUpdatePriorita, MessaggioResponse, MessaggioCreate
from app.models import Cliente, Operatore, Priorita
from app.crud.crud_segnalazione import create_messaggio, create_segnalazione, get_logs_by_segnalazione, get_segnalazione_by_id, get_segnalazioni, get_segnalazione_by_cliente, update_stato_segnalazione, update_priorita_segnalazione
from app.dependencies import get_db, get_current_user


router = APIRouter()

@router.post("/", response_model=SegnalazioneDetail)
async def crea_nuova_segnalazione(
    segnalazione_in: SegnalazioneCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user = Depends(get_current_user)
):
    if not isinstance(current_user, Cliente):
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Solo i clienti possono creare segnalazioni"
        )
    
    autore = f"{current_user.nome} {current_user.cognome}"
    
    nuova_segnalazione = await create_segnalazione(
        db = db,
        segnalazione_in = segnalazione_in,
        id_cliente = current_user.id,
        id_stato_iniziale = 1,
        autore = autore
    )

    return nuova_segnalazione

@router.get("/", response_model=list[SegnalazioneMinimal])
async def leggi_segnalazioni(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user = Depends(get_current_user), 
    id_stato: int|None = None,
    priorita: Priorita|None = None
):
    if isinstance(current_user, Cliente):
        return await get_segnalazione_by_cliente(db=db, id_stato = id_stato, priorita = priorita, id_cliente=current_user.id)

    if isinstance(current_user, Operatore):
        return await get_segnalazioni(db=db, id_stato = id_stato, priorita = priorita)
    
@router.get("/{segnalazione_id}", response_model=SegnalazioneDetail)
async def leggi_segnalazione(
    db: Annotated[AsyncSession, Depends(get_db)],
    id_segnalazione: int,
    current_user = Depends(get_current_user)
): 
    
    segnalazione = await get_segnalazione_by_id(db=db, id_segnalazione=id_segnalazione)

    if not segnalazione:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Segnalazione non trovata."
        )
    
    if isinstance(current_user, Cliente):
        if segnalazione.id_cliente != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Puoi leggere solo le tue segnalazioni."
            )
        
    return segnalazione
    
@router.put("/{id_segnalazione}/aggiorna_stato", response_model=SegnalazioneUpdateStato)
async def aggiorna_stato_segnalazione(
    db: Annotated[AsyncSession, Depends(get_db)],
    nuovo_stato: SegnalazioneUpdateStato,
    id_segnalazione: int,
    current_user = Depends(get_current_user)
):
    if not isinstance(current_user, Operatore): 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Solo gli operatori possono modificare lo stato della segnalazione"
        )
    
    operatore = f"{current_user.nome} {current_user.cognome}"
    
    return await update_stato_segnalazione(
        db=db, 
        id_segnalazione=id_segnalazione, 
        nuovo_stato=nuovo_stato, 
        operatore = operatore
    )

@router.put("/{id_segnalazione}/aggiorna_priorita", response_model=SegnalazioneUpdatePriorita)
async def aggiorna_priorita_segnalazione(
    db: Annotated[AsyncSession, Depends(get_db)],
    id_segnalazione: int,
    nuova_priorita: SegnalazioneUpdatePriorita,
    current_user = Depends(get_current_user),
):
    
    if isinstance(current_user, Cliente):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Solo gli operatori possono modificare la priorita della segnalazione"                
        )
    
    operatore = f"{current_user.nome} {current_user.cognome}"
    
    return await update_priorita_segnalazione(
        db=db,
        id_segnalazione=id_segnalazione, 
        nuova_priorita=nuova_priorita,
        operatore = operatore
    )

@router.post("/{id_segnalazione}/messaggi", response_model=MessaggioResponse)
async def scrivi_nuovo_messaggio(
    db: Annotated[AsyncSession, Depends(get_db)],
    id_segnalazione: int,
    messaggio_in: MessaggioCreate,
    current_user = Depends(get_current_user),
    
):
    
    segnalazione = await get_segnalazione_by_id(db=db, id_segnalazione=id_segnalazione)
    if not segnalazione: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Segnalazione non trovata"
        )
    
    if isinstance(current_user, Cliente):
        if segnalazione.id_cliente != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail = "Questa segnalazione non appartiene a te."
            )

    autore = f"{current_user.nome} {current_user.cognome}"

    if isinstance(current_user, Cliente):
        ruolo = "Cliente"
    elif isinstance(current_user, Operatore):
        ruolo = "Operatore"

    nuovo_messaggio = await create_messaggio(
        db=db, 
        id_segnalazione=id_segnalazione,
        contenuto=messaggio_in.contenuto,
        autore = autore,
        ruolo = ruolo
    )

    return nuovo_messaggio

@router.get("/{id_segnalazione}/log_segnalazione", response_model=LogStatoSegnalazioneResponse)
async def leggi_log_segnalazione(
    db: Annotated[AsyncSession, Depends(get_db)],
    id_segnalazione: int,
    current_user = Depends(get_current_user)
):
    
    if not isinstance(current_user, Operatore):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail = "Solo gli operatori possono visualizzare i log della segnalazione."
        )
    
    log_segnalazione = await get_logs_by_segnalazione(db=db, id_segnalazione=id_segnalazione)
    return log_segnalazione