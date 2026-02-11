from pydantic import BaseModel, EmailStr, ConfigDict, Field, field_validator
from pydantic_core import PydanticCustomError
import re
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

    @field_validator("password") 
    @classmethod 
    def validate_password(cls, value): 
        if len(value) < 8: 
            raise PydanticCustomError("password_too_short", "La password deve essere lunga almeno 8 caratteri") 
        if not re.search(r"[A-Z]", value):
            raise PydanticCustomError("password_no_uppercase","La password deve contenere almeno una lettera maiuscola")
        if not re.search(r"[a-z]", value):
            raise PydanticCustomError("password_no_lowercase", "La password deve contenere almeno una lettera minuscola")
        if not re.search(r"[0-9]", value): 
            raise PydanticCustomError("password_no_number", "La password deve contenere almeno un numero")
        if not re.search(r"[\W_]", value): 
            raise PydanticCustomError("password_no_special", "La password deve contenere almeno un carattere speciale")        
        return value

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

    @field_validator("contenuto") 
    @classmethod 
    def validate_contenuto(cls, value): 
        if len(value) < 10: 
            raise PydanticCustomError("messaggio_too_short", "Il messaggio deve essere lungo almeno 10 caratteri") 
        return value

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

    @field_validator("titolo") 
    @classmethod 
    def validate_titolo(cls, value): 
        if len(value) < 10: 
            raise PydanticCustomError("titolo_too_short", "Il titolo deve essere lungo almeno 10 caratteri") 
        return value

class SegnalazioneCreate(SegnalazioneBase):
    descrizione: str

    @field_validator("descrizione") 
    @classmethod 
    def validate_descrizione(cls, value): 
        if len(value) < 10: 
            raise PydanticCustomError("descrizione_too_short", "La descrizione deve essere lunga almeno 10 caratteri") 
        return value

class SegnalazioneMinimal(SegnalazioneBase):
    id: int
    priorita: Priorita
    data_apertura: datetime
    stato: StatoSegnalazioneResponse
    cliente: ClienteResponse
    operatore: Optional[str]=None
    model_config=ConfigDict(from_attributes=True)

class SegnalazioneDetail(SegnalazioneMinimal):
    descrizione: str
    messaggi: list[MessaggioResponse] = []

    @field_validator("descrizione") 
    @classmethod 
    def validate_descrizione(cls, value): 
        if len(value) < 10: 
            raise PydanticCustomError("descrizione_too_short", "La descrizione deve essere lunga almeno 10 caratteri") 
        return value

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


#===========================================================================
#                            SCHEMA USER GENERICO
#===========================================================================

class User(BaseModel):
    id: int
    nome: str
    cognome: str
    email: EmailStr
    ruolo: str
    model_config=ConfigDict(from_attributes=True)