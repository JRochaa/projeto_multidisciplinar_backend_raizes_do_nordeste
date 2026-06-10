from sqlalchemy import Column, Integer, String
from app.database.connection import Base


class Usuario(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    telefone = Column(String(20), nullable=True)
    endereco = Column(String(255), nullable=True)
    senha = Column(String, nullable=False)