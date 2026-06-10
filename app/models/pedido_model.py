from sqlalchemy import Column, Integer, ForeignKey, String, Numeric
from sqlalchemy.orm import relationship

from app.database.connection import Base


# Classe que representa a tabela "pedidos" no banco de dados.
class Pedido(Base):
    __tablename__ = "pedidos"

    # Chave primária da tabela.
    id = Column(Integer, primary_key=True, index=True)
    # Chave estrangeira que liga o pedido a um cliente.
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    # Status inicial do pedido.
    status = Column(String(50), nullable=False, default="PENDENTE")
    # Será calculado com base nos itens do pedido.
    valor_total = Column(Numeric(10, 2), nullable=False, default=0)
    # Relacionamento com a tabela clientes.
    cliente = relationship("Usuario") 
    itens = relationship("ItemPedido", back_populates="pedido")# Relacionamento com os itens do pedido. Permite acessar os itens usando pedido.itens.