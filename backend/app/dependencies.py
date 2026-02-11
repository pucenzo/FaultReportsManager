from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status

from app.core.db import SessionLocal
from app.core.security import decode_access_token
from app.crud.crud_cliente import get_cliente_by_email
from app.crud.crud_operatore import get_operatore_by_email

"""
Iniezione della dipendenza per la gestione della sessione del db.
Assicuriamo che la connessione venga chiusa alla fine di ogni richiesta.
"""
async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

"""
Ricava le informazioni dell'utente dai dati del token. 
Verifica la validità del token.
Verifica la presenza dell'utente nel db
"""
async def get_current_user(
    db: Annotated[AsyncSession, Depends(get_db)],
    token: Annotated[str,Depends(oauth2_scheme)],
):
    exception_message = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenziali non valide",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token=token)

        if payload is None:
            raise exception_message
            
        email = payload.sub
        role = payload.role

        if email is None or role is None:
            raise exception_message
    except JWTError:
        raise exception_message
    
    if role == "cliente":
        utente = await get_cliente_by_email(db, email=email)
    
    if role == "operatore":
        utente = await get_operatore_by_email(db, email=email)

    if utente is None:  
        raise exception_message
    
    return utente
