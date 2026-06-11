from pydantic import BaseModel, EmailStr, Field

from typing import Optional
from enum import Enum

# Enum que define os perfis possíveis de usuário.
class PerfilUsuarioEnum(str, Enum):
    ADMINISTRADOR = "ADMINISTRADOR"
    CLIENTE = "CLIENTE"

# Schema base com os campos comuns de cliente.
class ClienteBase(BaseModel):
    nome: str
    email: EmailStr
    telefone: Optional[str] = None
    endereco: Optional[str] = None

# Schema usado quando a API recebe dados para criar um cliente.
class ClienteCreate(ClienteBase):
    # A senha será criptografada antes de ser salva no banco.
    senha:  str = Field(min_length=6, max_length=72)


# Schema usado quando a API devolve um cliente como resposta.
class ClienteResponse(ClienteBase):
    id: int

    # Perfil do usuário retornado na resposta.
    perfil: PerfilUsuarioEnum
    
    # Permite que o Pydantic leia dados vindos de objetos SQLAlchemy.Sem isso, ele espera apenas dicionários.
    class Config:
        from_attributes = True