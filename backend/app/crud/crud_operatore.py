from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from app.schemas import OperatoreCreate
from app.models import Operatore
from app.core.security import get_password_hash

"""
Crea un operatore nel sistema. 
Utilizza lo schema OperatoreCreate per la validazione dei dati in ingresso.
Gestisce l'hashing della password, la creazione del modello e la memorizzazione
"""
async def create_operatore(
    db: AsyncSession,
    operatore_in: OperatoreCreate
) -> Operatore:
    
    password_hashata = get_password_hash(operatore_in.password)

    db_operatore = Operatore(
        nome = operatore_in.nome,
        cognome = operatore_in.cognome,
        email = operatore_in.email,
        hashed_pw = password_hashata
    )

    db.add(db_operatore)
    await db.commit()
    await db.refresh(db_operatore)

    return db_operatore

"""recupera l'operatore tramite l'email"""
async def get_operatore_by_email(
    db: AsyncSession, 
    email: str
) -> Operatore|None:
    
    query = select(Operatore).where(Operatore.email == email)
    result = await db.execute(query)
    return result.scalar_one_or_none()