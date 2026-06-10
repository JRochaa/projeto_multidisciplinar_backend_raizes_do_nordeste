from sqlalchemy import Column, Integer, ForeignKey, String, Numeric
from sqlalchemy.orm import relationship

from app.database.connection import Base


class Pagamento(Base):
    __tablename__ = "pagamentos"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    status = Column(String(50), nullable=False, default="PENDENTE")
    metodo = Column(String(50), nullable=False)
    valor = Column(Numeric(10, 2), nullable=False)

    pedido = relationship("Pedido")