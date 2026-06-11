from pydantic import BaseModel
from decimal import Decimal


# Schema usado quando a API recebe os dados para processar um pagamento. O pedido_id informa qual pedido será pago.
# O metodo indica a forma de pagamento, por exemplo: PIX, CARTAO ou BOLETO.
class PagamentoCreate(BaseModel):
    pedido_id: int
    metodo: str


# Schema usado quando a API devolve o pagamento processado. Aqui aparecem o id, status e valor final do pagamento.
class PagamentoResponse(BaseModel):
    id: int
    pedido_id: int
    metodo: str
    status: str
    valor: Decimal

    class Config:
        from_attributes = True

#Schema usado no processamento do pagamento, avisa se o pagamento foi "APROVADO" ou "RECUSADO".
class PagamentoProcessamentoResponse(PagamentoResponse):
    mensagem: str        