from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.produto_schema import ProdutoCreate, ProdutoResponse
from app.repositories.produto_repository import (
    buscar_produto_por_id,
    criar_produto,
    listar_produtos,
)


# prefix="/produtos" faz todas as rotas começarem com /produtos.
# tags=["Produtos"] agrupa essas rotas no Swagger.
router = APIRouter(
    prefix="/produtos",
    tags=["Produtos"]
)


# Rota para listar todos os produtos cadastrados.
@router.get("/", response_model=list[ProdutoResponse])
def listar(db: Session = Depends(get_db)):
    # Retorna todos os produtos salvos no banco.
    return listar_produtos(db)


# Rota para buscar um produto específico pelo id.
@router.get("/{produto_id}", response_model=ProdutoResponse)
def buscar_por_id(produto_id: int, db: Session = Depends(get_db)):
    # Busca o produto pelo id informado na URL.
    produto = buscar_produto_por_id(db, produto_id)

    if produto is None:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado."
        )

    return produto


# Rota para cadastrar um novo produto.
@router.post("/", response_model=ProdutoResponse, status_code=201)
def criar(produto: ProdutoCreate, db: Session = Depends(get_db)):
    # Cria um novo produto no banco usando o repository.
    return criar_produto(db, produto)