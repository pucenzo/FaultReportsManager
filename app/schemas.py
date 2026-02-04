from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from app.models import Priorita
from datetime import datetime

#===========================================================================
#                               SCHEMI CLIENTE
#===========================================================================

class ClienteBase(BaseModel):
    nome: str
    cognome: str
    email: EmailStr

class ClienteCreate(ClienteBase):
    password: str

class ClienteResponse(ClienteBase):
    id: int
    model_config=ConfigDict(from_attributes=True)

#===========================================================================
#                               SCHEMI OPERATORE
#===========================================================================

class OperatoreBase(BaseModel):
    nome: str
    cognome: str
    email: str

class OperatoreCreate(OperatoreBase):
    password: str

class OperatoreResponse(OperatoreBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

#===========================================================================
#                              SCHEMI STATO SEGNALAZIONE
#===========================================================================

class StatoSegnalazioneResponse(BaseModel):
    id: int
    nome: str
    model_config=ConfigDict(from_attributes=True)
    
#===========================================================================
#                            SCHEMI MESSAGGI
#===========================================================================

class MessaggioBase(BaseModel):
    contenuto: str

class MessaggioCreate(MessaggioBase):
    pass

class MessaggioResponse(MessaggioBase):
    id: int
    data_invio: datetime
    autore: str
    ruolo: str
    id_segnalazione: int
    model_config = ConfigDict(from_attributes=True)

#===========================================================================
#                               SCHEMI SEGNALAZIONE
#===========================================================================

class SegnalazioneBase(BaseModel):
    titolo: str

class SegnalazioneCreate(SegnalazioneBase):
    descrizione: str

class SegnalazioneMinimal(SegnalazioneBase):
    id: int
    priorita: Priorita
    data_apertura: datetime
    stato: StatoSegnalazioneResponse
    cliente: ClienteResponse
    model_config=ConfigDict(from_attributes=True)

class SegnalazioneDetail(SegnalazioneMinimal):
    descrizione: str
    messaggi: list[MessaggioResponse] = []

class SegnalazioneUpdatePriorita(BaseModel):
    priorita: Priorita

class SegnalazioneUpdateStato(BaseModel):
    id_stato: int

#===========================================================================
#                           SCHEMI LOG STATI SEGNALAZIONE
#===========================================================================

class LogStatoSegnalazioneResponse(BaseModel):
    id: int
    vecchio_stato: Optional[str]=None
    nuovo_stato: str
    data_modifica: datetime
    id_segnalazione: int
    operatore: str
    model_config=ConfigDict(from_attributes=True)

#===========================================================================
#                            SCHEMI TOKEN AUTENTICAZIONE
#===========================================================================

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    sub: Optional[str] = None 
    role: Optional[str] = None
    id: Optional[int] = None