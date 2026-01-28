from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class Priorita (str, Enum):
    BASSA = "Bassa"
    MEDIA = "Media"
    ALTA = "Alta"

class SegnalazioneBase(BaseModel):
    titolo: str
    descrizione: str

class SegnalazionePrioritaUpdate(BaseModel):
    priorita: Optional[Priorita] = None

class SegnalazioneStatoUpdate(BaseModel):
    id_nuovo_stato: int

class SegnalazioneCreate(SegnalazioneBase):
    id_cliente = id

class SegnalazioneResponse(SegnalazioneBase):
    id: int
    priorita = Priorita
    data_apertura: datetime
    stato: Optional[StatoResponse] = None
    