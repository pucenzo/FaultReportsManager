from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_current_user
from app.schemas import User
from app.models import Cliente

router = APIRouter()

"""
Endpoint per leggere le informazioni dell'utente.
Utilizza lo schema User per la validazione dei dati in output.
"""
@router.get("/user/me", response_model=User)
async def read_user(
    current_user = Depends(get_current_user)
):
    
    if isinstance(current_user, Cliente):
        ruolo = "cliente"
    else:
        ruolo = "operatore"

    return User(
        id=current_user.id,
        nome=current_user.nome,
        cognome=current_user.cognome,
        email=current_user.email,
        ruolo=ruolo
    )