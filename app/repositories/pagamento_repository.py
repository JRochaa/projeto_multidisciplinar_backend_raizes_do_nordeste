from sqlalchemy.orm import Session

from app.models.pagamento_model import Pagamento
from app.schemas.pagamento_schema import PagamentoCreate
from app.repositories.pedido_repository import buscar_pedido_por_id
from random import choice

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

    
    # Simulação de pagamento mock com aleatoriedade para aprovar e recusar o pagamento as vezes.
    status_pagamento = choice([
        "APROVADO",
        "APROVADO",
        "RECUSADO"
    ])

    # Cria o pagamento usando o valor total do pedido.
    novo_pagamento = Pagamento(
        pedido_id=pedido.id,
        metodo=pagamento.metodo,
        status=status_pagamento,
        valor=pedido.valor_total
    )

    db.add(novo_pagamento)

    # Atualiza o status do pedido para PAGO.
    if status_pagamento == "APROVADO":
        pedido.status = "PAGO"

    db.commit()

    db.refresh(novo_pagamento)

    if status_pagamento == "APROVADO":
        novo_pagamento.mensagem = "Pagamento aprovado com sucesso."
    else:
        novo_pagamento.mensagem = "Pagamento recusado. O pedido permanece pendente e pode ser pago novamente."

    return novo_pagamento