from app.core.db import Base
from sqlalchemy import Column, Integer, String, Enum as SQLAlchemyEnum, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from enum import Enum

class Priorita(str, Enum):
    BASSA = "Bassa"
    MEDIA = "Media"
    ALTA = "Alta"

class Segnalazione(Base):
    __tablename__ = "segnalazioni"

    id = Column(Integer, primary_key=True, index=True)
    titolo = Column(String, nullable = False)
    descrizione = Column(Text, nullable = False)
    priorita = Column(SQLAlchemyEnum(Priorita), nullable = False, default = Priorita.BASSA)
    data_apertura = Column(DateTime, default=lambda:datetime.now(timezone.utc))

    id_cliente = Column(Integer, ForeignKey("clienti.id"))
    id_stato = Column(Integer, ForeignKey("stati_segnalazione.id"))

    cliente = relationship("Cliente", back_populates = "segnalazioni")
    stato = relationship("StatoSegnalazione", back_populates = "segnalazioni")
    logs = relationship("LogStatoSegnalazione", back_populates="segnalazione")
    messaggi = relationship("Messaggio", back_populates = "segnalazione")


class Cliente(Base):
    __tablename__= 'clienti'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cognome = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    hashed_pw = Column(String, nullable=False)

    segnalazioni = relationship("Segnalazione", back_populates = "cliente")

class Operatore(Base):
    __tablename__="operatori"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cognome = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    hashed_pw = Column(String, nullable=False)

class LogStatoSegnalazione(Base):
    __tablename__ = "logs_stato_segnalazioni"

    id = Column(Integer, primary_key=True, index=True)
    vecchio_stato = Column(String, nullable=True)
    nuovo_stato = Column(String, nullable=False)
    data_modifica = Column(DateTime, nullable=False, default= lambda:datetime.now(timezone.utc))

    id_segnalazione = Column(Integer, ForeignKey("segnalazioni.id"))
    id_operatore = Column(String)

    segnalazione = relationship("Segnalazione", back_populates="logs")

class StatoSegnalazione(Base):
    __tablename__ = "stati_segnalazione"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, unique = True)

    segnalazioni=relationship("Segnalazione", back_populates = "stato")

class Messaggio(Base):
    __tablename__ = "messaggi"

    id = Column(Integer, primary_key=True, index=True)
    contenuto = Column(Text, nullable=False)
    data_invio = Column(DateTime, nullable=False, default = lambda: datetime.now(timezone.utc))
    autore = Column(String, nullable=False)
    ruolo = Column(String, nullable=False)

    id_segnalazione = Column(Integer, ForeignKey("segnalazioni.id"))

    segnalazione = relationship("Segnalazione", back_populates="messaggi")