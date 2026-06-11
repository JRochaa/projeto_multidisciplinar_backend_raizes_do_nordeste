from sqlalchemy.orm import Session

from app.models.usuario_model import Usuario
from app.schemas.usuario_schema import ClienteCreate


# Busca todos os clientes cadastrados no banco.
def listar_clientes(db: Session):
    return db.query(Usuario).all()


# Busca um cliente pelo id. Retorna o cliente se encontrar, ou None se não existir.
def buscar_cliente_por_id(db: Session, usuario_id: int):
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()


# Busca um cliente pelo email. Isso será útil para evitar cadastro duplicado.
def buscar_cliente_por_email(db: Session, email: str):
    return db.query(Usuario).filter(Usuario.email == email).first()


# Cria um novo cliente no banco de dados.
def criar_cliente(db: Session, cliente: ClienteCreate):
    # Cria um objeto Cliente a partir dos dados recebidos pelo schema.
    novo_cliente = Usuario(
        nome=cliente.nome,
        email=cliente.email,
        telefone=cliente.telefone,
        endereco=cliente.endereco,
        senha=cliente.senha,
        perfil="CLIENTE"
    )

    # Adiciona o novo cliente à sessão do banco.
    db.add(novo_cliente)
    # Confirma a operação no banco.
    db.commit()
    # Atualiza o objeto Python com os dados gerados pelo banco, como o id.
    db.refresh(novo_cliente)

    return novo_cliente