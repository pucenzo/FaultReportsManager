from database.database import Base
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship

class StatoSegnalazione(Base):
    __tablename__ = "stato_segnalazione"

    id = Column(Integer, primary_key=True, index=True)
    stato = Column(String, nullable=False)

    segnalazioni=relationship("Segnalazione", back_populates = "stato")