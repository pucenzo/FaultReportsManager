from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.schemas import SegnalazioneResponse, SegnalazioneCreate, SegnalazioneUpdateStato, SegnalazioneUpdatePriorita
from app.models import Cliente, Operatore, Priorita
from app.crud.crud_segnalazione import create_segnalazione, get_segnalazioni, get_segnalazione_by_cliente, update_stato_segnalazione, update_priorita_segnalazione
from app.dependencies import get_db, get_current_user


router = APIRouter()

@router.post("/", response_model=SegnalazioneResponse)
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
    
    nuova_segnalazione = await create_segnalazione(
        db = db,
        segnalazione_in = segnalazione_in,
        id_cliente = current_user.id,
        id_stato_iniziale = 1
    )

    return nuova_segnalazione

@router.get("/", response_model=list[SegnalazioneResponse])
async def leggi_segnalazioni(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user = Depends(get_current_user), 
    id_stato: int|None = None,
    priorita: Priorita|None = None
):
    if isinstance(current_user, Cliente):
        return await get_segnalazione_by_cliente(db=db, id_cliente=current_user.id)

    if isinstance(current_user, Operatore):
        return await get_segnalazioni(db=db, id_stato = id_stato, priorita = priorita)
        
    
@router.put("/{id_segnalazione}/aggiorna_stato", response_model=SegnalazioneResponse)
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
    
    return await update_stato_segnalazione(
        db=db, 
        id_segnalazione=id_segnalazione, 
        nuovo_stato=nuovo_stato
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
    
    return await update_priorita_segnalazione(
        db=db,
        id_segnalazione=id_segnalazione, 
        nuova_priorita=nuova_priorita
    )