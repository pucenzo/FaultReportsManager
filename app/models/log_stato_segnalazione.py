from database.database import Base
from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from datetime import datetime
class LogStatoSegnalazione(Base):
    __tablename__ = "log_stato_segnalazione"

    id = Column(Integer, primary_key=True, index=True)
    vecchio_stato = Column(String, nullable=True)
    nuovo_stato = Column(String, nullable=False)
    data_modifica = Column(DateTime, nullable=False, default=datetime.utcnow)
    id_segnalazione = Column(Integer, ForeignKey("segnalazione.id"))