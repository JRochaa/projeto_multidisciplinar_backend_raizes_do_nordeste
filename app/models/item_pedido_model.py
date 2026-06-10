from sqlalchemy import Column, Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship

from app.database.connection import Base


# Classe que representa a tabela "itens_pedido". Essa tabela liga pedidos e produtos.
class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    id = Column(Integer, primary_key=True, index=True)

    # Chave estrangeira que liga o item a um pedido.
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    # Chave estrangeira que liga o item a um produto.
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    # Quantidade comprada daquele produto.
    quantidade = Column(Integer, nullable=False)
    # Preço do produto no momento da compra.
    preco_unitario = Column(Numeric(10, 2), nullable=False)
    # Relacionamento com pedido.
    pedido = relationship("Pedido", back_populates="itens")
    # Relacionamento com produto.
    produto = relationship("Produto")