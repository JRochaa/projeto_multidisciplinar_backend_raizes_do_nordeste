from sqlalchemy.orm import Session

from app.models.produto_model import Produto
from app.schemas.produto_schema import ProdutoCreate


# Busca todos os produtos cadastrados no banco.
def listar_produtos(db: Session):
    return db.query(Produto).all()


# Busca um produto pelo id. Retorna o produto se encontrar, ou None se não existir.
def buscar_produto_por_id(db: Session, produto_id: int):
    return db.query(Produto).filter(Produto.id == produto_id).first()


# Cria um novo produto no banco de dados.
def criar_produto(db: Session, produto: ProdutoCreate):
    # Cria um objeto Produto a partir dos dados recebidos pelo schema.
    novo_produto = Produto(
        nome=produto.nome,
        descricao=produto.descricao,
        preco=produto.preco,
        estoque=produto.estoque
    )

    db.add(novo_produto)

    db.commit()

    db.refresh(novo_produto)

    return novo_produto


# Atualiza o estoque de um produto. Será usado quando um pedido for criado.
def atualizar_estoque_produto(db: Session, produto: Produto, nova_quantidade: int):
    # Altera o valor do estoque no objeto Produto.
    produto.estoque = nova_quantidade

    db.commit()

    db.refresh(produto)

    return produto