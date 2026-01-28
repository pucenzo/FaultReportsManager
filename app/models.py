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
    __tablename__ = "segnalazione"

    id = Column(Integer, primary_key=True, index=True)
    titolo = Column(String, nullable = False)
    descrizione = Column(Text, nullable = False)
    priorita = Column(SQLAlchemyEnum(Priorita), nullable = False)
    data_apertura = Column(DateTime, default=lambda:datetime.now(timezone.utc))

    id_cliente = Column(Integer, ForeignKey("cliente.id"))
    id_stato = Column(Integer, ForeignKey("stato_segnalazione.id"))

    cliente = relationship("Cliente", back_populates = "segnalazioni")
    stato = relationship("StatoSegnalazione", back_populates = "segnalazioni")


class Cliente(Base):
    __tablename__= 'cliente'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cognome = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)

    segnalazioni = relationship("Segnalazione", back_populates = "cliente")

class LogStatoSegnalazione(Base):
    __tablename__ = "log_stato_segnalazione"

    id = Column(Integer, primary_key=True, index=True)
    vecchio_stato = Column(String, nullable=True)
    nuovo_stato = Column(String, nullable=False)
    data_modifica = Column(DateTime, nullable=False, default= lambda:datetime.now(timezone.utc))
    id_segnalazione = Column(Integer, ForeignKey("segnalazione.id"))


class StatoSegnalazione(Base):
    __tablename__ = "stato_segnalazione"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, unique = True)

    segnalazioni=relationship("Segnalazione", back_populates = "stato")