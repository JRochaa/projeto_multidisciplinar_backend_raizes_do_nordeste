from sqlalchemy.orm import Session

from app.models.pagamento_model import Pagamento
from app.schemas.pagamento_schema import PagamentoCreate
from app.repositories.pedido_repository import buscar_pedido_por_id


# Lista todos os pagamentos cadastrados.
def listar_pagamentos(db: Session):
    return db.query(Pagamento).all()


# Busca um pagamento pelo id. Retorna o pagamento se encontrar, ou None se não existir.
def buscar_pagamento_por_id(db: Session, pagamento_id: int):
    return db.query(Pagamento).filter(Pagamento.id == pagamento_id).first()


# Cria um pagamento para um pedido.
def criar_pagamento(db: Session, pagamento: PagamentoCreate):
    # Busca o pedido relacionado ao pagamento.
    pedido = buscar_pedido_por_id(db, pagamento.pedido_id)

    # Se o pedido não existir, desfaz a operação e lança erro.
    if pedido is None:
        raise ValueError(f"Pedido com id {pagamento.pedido_id} não encontrado.")

    # Se o pedido já estiver pago, evita pagar duas vezes.
    if pedido.status == "PAGO":
        raise ValueError("Este pedido já está pago.")

    # Como é um pagamento simulado, vamos aprovar automaticamente.
    status_pagamento = "APROVADO"

    # Cria o pagamento usando o valor total do pedido.
    novo_pagamento = Pagamento(
        pedido_id=pedido.id,
        metodo=pagamento.metodo,
        status=status_pagamento,
        valor=pedido.valor_total
    )

    db.add(novo_pagamento)

    # Atualiza o status do pedido para PAGO.
    pedido.status = "PAGO"

    db.commit()

    db.refresh(novo_pagamento)

    return novo_pagamento