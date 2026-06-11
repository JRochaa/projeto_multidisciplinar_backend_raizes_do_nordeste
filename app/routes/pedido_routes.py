from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.repositories.pedido_repository import (
    listar_pedidos,
    buscar_pedido_por_id,
    criar_pedido
)
from app.schemas.pedido_schema import PedidoCreate, PedidoResponse, CanalPedidoEnum


#Rota específico para as rotas de pedidos, prefix="/pedidos" significa que todas as rotas deste arquivo começam com /pedidos.
# tags=["Pedidos"] organiza essas rotas no Swagger.
router = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos"]
)


# Rota para listar todos os pedidos cadastrados, também permite filtar os pedidos pelo canal.
@router.get("/", response_model=list[PedidoResponse])
def listar(
    canalPedido: CanalPedidoEnum | None = None,
    db: Session = Depends(get_db)
):
    # Se canalPedido foi informado, usamos canalPedido.value.
    # Exemplo: CanalPedidoEnum.TOTEM vira "TOTEM".
    canal = canalPedido.value if canalPedido else None

    return listar_pedidos(db, canal)


# Rota para buscar um pedido específico pelo ID.
@router.get("/{pedido_id}", response_model=PedidoResponse)
def buscar_por_id(pedido_id: int, db: Session = Depends(get_db)):
    # Busca o pedido no banco.
    pedido = buscar_pedido_por_id(db, pedido_id)

    # Se o pedido não existir, retorna erro 404.
    if pedido is None:
        raise HTTPException(status_code=404, detail="Pedido não encontrado.")

    return pedido


# Rota para criar um novo pedido.
@router.post("/", response_model=PedidoResponse, status_code=201)
def criar(pedido: PedidoCreate, db: Session = Depends(get_db)):
    try:
        # Chama o repository que cria o pedido, calcula total e baixa estoque.
        novo_pedido = criar_pedido(db, pedido)

        return novo_pedido

    except ValueError as erro:
        # Captura erros gerados no repository, como produto inexistente ou estoque insuficiente.
        raise HTTPException(status_code=400, detail=str(erro))