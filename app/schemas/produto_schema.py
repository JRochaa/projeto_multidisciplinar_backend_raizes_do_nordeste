from pydantic import BaseModel
from typing import Optional
from decimal import Decimal


# Schema base com os campos comuns de produto.
class ProdutoBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    preco: Decimal
    estoque: int



class ProdutoCreate(ProdutoBase):
    pass


# Schema usado quando a API devolve um produto cadastrado.
class ProdutoResponse(ProdutoBase):
    id: int

    # Converte objetos SQLAlchemy em resposta JSON.
    class Config:
        from_attributes = True