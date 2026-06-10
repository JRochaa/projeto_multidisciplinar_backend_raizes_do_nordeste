from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.usuario_schema import ClienteCreate, ClienteResponse
from app.repositories.usuario_repository import (
    buscar_cliente_por_email,
    buscar_cliente_por_id,
    criar_cliente,
    listar_clientes,
)
from app.services.auth_service import gerar_hash_senha


# APIRouter organiza as rotas relacionadas a clientes. prefix="/ususarios" faz todas as rotas começarem com /clientes.
# tags=["Usuarios"] agrupa essas rotas no Swagger.
router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)


# Rota para listar todos os clientes cadastrados.
# response_model informa o formato da resposta no Swagger.
@router.get("/", response_model=list[ClienteResponse])
def listar(db: Session = Depends(get_db)):
    # db recebe uma sessão do banco usando a função get_db.
    return listar_clientes(db)


# Rota para buscar um cliente específico pelo id.
@router.get("/{cliente_id}", response_model=ClienteResponse)
def buscar_por_id(cliente_id: int, db: Session = Depends(get_db)):
    # Busca o cliente no banco usando o repository.
    cliente = buscar_cliente_por_id(db, cliente_id)

    # Se não encontrar, retorna erro 404.
    if cliente is None:
        raise HTTPException(
            status_code=404,
            detail="Cliente não encontrado."
        )

    return cliente


# Rota para cadastrar um novo cliente.
@router.post("/", response_model=ClienteResponse, status_code=201)
def criar(cliente: ClienteCreate, db: Session = Depends(get_db)):
    # Verifica se já existe um cliente com o mesmo email.
    cliente_existente = buscar_cliente_por_email(db, cliente.email)

    # Se o email já estiver cadastrado, retorna erro 400.
    if cliente_existente:
        raise HTTPException(
            status_code=400,
            detail="Já existe um cliente cadastrado com este email."
        )
    
    # Criptografa a senha antes de salvar no banco
    cliente.senha = gerar_hash_senha(cliente.senha)

    # Cria o cliente no banco usando o repository.
    return criar_cliente(db, cliente)