from database.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Cliente(Base):
    __tablename__= 'cliente'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cognome = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)

    segnalazioni = relationship("Segnalazione", back_populates = "cliente")