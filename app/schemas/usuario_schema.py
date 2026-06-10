from pydantic import BaseModel, EmailStr, Field
from typing import Optional


# Schema base com os campos comuns de cliente.
class ClienteBase(BaseModel):
    nome: str
    email: EmailStr
    telefone: Optional[str] = None
    endereco: Optional[str] = None
    senha:  str = Field(min_length=6, max_length=72)

# Schema usado quando a API recebe dados para criar um cliente.
class ClienteCreate(ClienteBase):
    pass


# Schema usado quando a API devolve um cliente como resposta.
class ClienteResponse(ClienteBase):
    id: int

    # Permite que o Pydantic leia dados vindos de objetos SQLAlchemy.Sem isso, ele espera apenas dicionários.
    class Config:
        from_attributes = True