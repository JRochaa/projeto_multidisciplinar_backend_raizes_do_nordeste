from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.repositories.pagamento_repository import (
    listar_pagamentos,
    buscar_pagamento_por_id,
    criar_pagamento
)
from app.schemas.pagamento_schema import PagamentoCreate, PagamentoResponse


#Rota específico para as rotas de pagamentos, prefix="/pagamentos" significa que todas as rotas deste arquivo começam com /pagamentos.
#tags=["Pagamentos"] organiza essas rotas no Swagger.
router = APIRouter(
    prefix="/pagamentos",
    tags=["Pagamentos"]
)


# Rota para listar todos os pagamentos cadastrados.
@router.get("/", response_model=list[PagamentoResponse])
def listar(db: Session = Depends(get_db)):
    # Chama o repository responsável por buscar os pagamentos no banco.
    return listar_pagamentos(db)


# Rota para buscar um pagamento específico pelo ID.
@router.get("/{pagamento_id}", response_model=PagamentoResponse)
def buscar_por_id(pagamento_id: int, db: Session = Depends(get_db)):
    # Busca o pagamento no banco usando o repository.
    pagamento = buscar_pagamento_por_id(db, pagamento_id)

    # Se o pagamento não existir, retorna erro 404.
    if pagamento is None:
        raise HTTPException(status_code=404, detail="Pagamento não encontrado.")

    return pagamento


# Rota para criar/processar um pagamento.
@router.post("/", response_model=PagamentoResponse, status_code=201)
def criar(pagamento: PagamentoCreate, db: Session = Depends(get_db)):
    try:
        # Chama o repository que cria o pagamento e atualiza o pedido para PAGO.
        novo_pagamento = criar_pagamento(db, pagamento)

        return novo_pagamento

    except ValueError as erro:
        # Captura erros como pedido inexistente ou pedido já pago.
        raise HTTPException(status_code=400, detail=str(erro))