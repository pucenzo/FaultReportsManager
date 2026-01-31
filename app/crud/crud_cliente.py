from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schemas import ClienteCreate, ClienteResponse
from app.models import Cliente
from app.core.security import get_password_hash

async def create_cliente(
  db: AsyncSession,
  cliente_in: ClienteCreate      
) -> Cliente:
    password_hashata = get_password_hash(cliente_in.password)

    db_cliente = Cliente(
        nome = cliente_in.nome,
        cognome = cliente_in.cognome, 
        email = cliente_in.email,
        hashed_pw = password_hashata,
    )

    db.add(db_cliente)
    await db.commit()
    await db.refresh(db_cliente)

    return db_cliente

async def get_cliente_by_email(
  db: AsyncSession,
  email: str      
) -> Cliente|None:
    
    query = select(Cliente).where(Cliente.email == email)
    result = await db.execute(query)
    return result.scalar_one_or_none()