from pydantic import BaseModel, Field
from decimal import Decimal


# Schema usado para receber os produtos dentro de um pedido.
# Aqui o usuário informa qual produto quer comprar e a quantidade.
class ItemPedidoCreate(BaseModel):
    produto_id: int
    quantidade: int = Field(gt=0)


# Schema usado para devolver os itens de um pedido já criado.
class ItemPedidoResponse(BaseModel):
    id: int
    pedido_id: int
    produto_id: int
    quantidade: int
    preco_unitario: Decimal


    class Config:
        from_attributes = True