from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta

from app.dependencies import get_db
from app.schemas import ClienteResponse, ClienteCreate, Token
from app.crud.crud_cliente import get_cliente_by_email, create_cliente
from app.crud.crud_operatore import get_operatore_by_email
from app.core.security import verify_password, create_access_token
from app.core.config import settings

router = APIRouter()

@router.post("/register", response_model=ClienteResponse)
async def register_cliente(
    cliente_in: ClienteCreate,
    db: AsyncSession = Depends(get_db)
):  
    cliente_esistente = await get_cliente_by_email(db, cliente_in.email)

    if cliente_esistente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Un cliente con questa email è già registrato"
        )
    
    nuovo_cliente = await create_cliente(db, cliente_in)

    return nuovo_cliente

@router.post("/login", response_model=Token)
async def login_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):

    utente = await get_cliente_by_email(db, form_data.username)
    
    ruolo = "cliente"

    if not utente: 
        utente = await get_operatore_by_email(db, form_data.username)
        ruolo = "operatore"
        
    if not utente or not verify_password(form_data.password, utente.hashed_pw):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o password non corrette. Riprova",
            headers={"WWW-Authenticate": "Bearer"},
            )
    
    access_token_expires = timedelta(minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        soggetto = utente.email,
        ruolo = ruolo, 
        id = utente.id,
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

        
