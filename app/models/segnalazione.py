from database.database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Enum as SQLAlchemyEnum, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

class Priorita(str, enum.Enum):
    BASSA = "Bassa"
    MEDIA = "Media"
    ALTA = "Alta"

class Segnalazione(Base):
    __tablename__ = "segnalazione"

    id = Column(Integer, primary_key=True, index=True)
    titolo = Column(String, nullable = False)
    descrizione = Column(Text, nullable = False)
    priorita = Column(SQLAlchemyEnum(Priorita), nullable = False)
    data_apertura = Column(DateTime, default=datetime.utcnow)

    id_cliente = Column(Integer, ForeignKey("cliente.id"))
    id_stato = Column(Integer, ForeignKey("stato_segnalazione.id"))

    cliente = relationship("Cliente", back_populates = "segnalazioni")
    stato = relationship("StatoSegnalazione", back_populates = "segnalazioni")