from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.repositories.pagamento_repository import (
    listar_pagamentos,
    buscar_pagamento_por_id,
    criar_pagamento
)
from app.schemas.pagamento_schema import PagamentoCreate, PagamentoResponse, PagamentoProcessamentoResponse
from app.routes.auth_routes import obter_cliente_logado, exigir_administrador
from app.repositories.pedido_repository import buscar_pedido_por_id


#Rota específico para as rotas de pagamentos, prefix="/pagamentos" significa que todas as rotas deste arquivo começam com /pagamentos.
#tags=["Pagamentos"] organiza essas rotas no Swagger.
router = APIRouter(
    prefix="/pagamentos",
    tags=["Pagamentos"]
)


# Rota para listar todos os pagamentos cadastrados. Apenas para administradores.
@router.get("/", response_model=list[PagamentoResponse])
def listar(db: Session = Depends(get_db), administrador = Depends(exigir_administrador)):

    # Chama o repository responsável por buscar os pagamentos no banco.
    return listar_pagamentos(db)


# Rota para buscar um pagamento específico pelo ID.
@router.get("/{pagamento_id}", response_model=PagamentoResponse)
def buscar_por_id(
    pagamento_id: int, 
    db: Session = Depends(get_db),
    cliente_logado = Depends(obter_cliente_logado)      
):
    # Busca o pagamento no banco usando o repository.
    pagamento = buscar_pagamento_por_id(db, pagamento_id)

    # Se o pagamento não existir, retorna erro 404.
    if pagamento is None:
        raise HTTPException(status_code=404, detail="Pagamento não encontrado.")
    
    pedido = buscar_pedido_por_id(db, pagamento.pedido_id)

    if pedido is None:
        raise HTTPException(status_code=404, detail="Pedido vinculado ao pagamento não encontrado.")

     # Se não for administrador, só pode acessar pagamento do próprio pedido.
    if cliente_logado.perfil != "ADMINISTRADOR" and pedido.cliente_id != cliente_logado.id:
        raise HTTPException(
            status_code=403,
            detail="Você não tem permissão para acessar este pagamento."
        )
    
    return pagamento


# Rota para criar/processar um pagamento.
# Cliente só pode pagar pedido próprio. Administrador pode pagar qualquer pedido.
@router.post("/", response_model=PagamentoProcessamentoResponse, status_code=201)
def criar(
    pagamento: PagamentoCreate, 
    db: Session = Depends(get_db),
    cliente_logado = Depends(obter_cliente_logado)
):
    try:
        pedido = buscar_pedido_por_id(db, pagamento.pedido_id)

        if pedido is None:
            raise HTTPException(
                status_code=400,
                detail=f"Pedido com id {pagamento.pedido_id} não encontrado."
            )
        
        
        if cliente_logado.perfil != "ADMINISTRADOR" and pedido.cliente_id != cliente_logado.id:
            raise HTTPException(
                status_code=403,
                detail="Cliente só pode pagar pedido próprio."
            )

        # Chama o repository que cria o pagamento e atualiza o pedido para PAGO.
        novo_pagamento = criar_pagamento(db, pagamento)

        return novo_pagamento

    except ValueError as erro:
        # Captura erros como pedido inexistente ou pedido já pago.
        raise HTTPException(status_code=400, detail=str(erro))