from pydantic import BaseModel, Field
from typing import List
from decimal import Decimal
from enum import Enum

from app.schemas.item_pedido_schema import ItemPedidoCreate, ItemPedidoResponse


# Enum que define os canais possíveis de origem do pedido.
class CanalPedidoEnum(str, Enum):
    APP = "APP"
    TOTEM = "TOTEM"
    BALCAO = "BALCAO"
    PICKUP = "PICKUP"
    WEB = "WEB"

# Schema usado quando a API recebe dados para criar um pedido. O cliente_id informa quem está fazendo o pedido.
# A lista de itens informa quais produtos serão comprados.
class PedidoCreate(BaseModel):
    cliente_id: int
    canalPedido: CanalPedidoEnum
    itens: List[ItemPedidoCreate] = Field(min_length=1)


# Schema usado quando a API devolve um pedido criado.
class PedidoResponse(BaseModel):
    id: int
    cliente_id: int
    canalPedido: CanalPedidoEnum
    status: str
    valor_total: Decimal
    itens: List[ItemPedidoResponse] = []

    class Config:
        from_attributes = True