import asyncio

from app.crud.crud_operatore import create_operatore
from app.core.db import SessionLocal
from app.schemas import OperatoreCreate

async def main():
    nome = input("Inserisci il nome dell'operatore: ")
    cognome = input("Inserisci il cognome dell'operatore: ")
    email = input("Inserisci l'email dell'operatore: ")
    password = input("Inserisci la password dell'operatore: ")

    async with SessionLocal() as db:
        try:
        
            dati_operatore = OperatoreCreate(
                nome=nome,
                cognome=cognome,
                email=email,
                password=password
            )

            operatore = await create_operatore(db, dati_operatore)
            print(f"Operatore creato con successo!")
        except Exception as e:
            print(f"Errore durante la creazione dell'operatore: {e}")
    
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Errore: {e}")
