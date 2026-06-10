from app.database.connection import engine, Base
from app.models import Usuario, Produto, Pedido, Pagamento, ItemPedido


def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas com sucesso!")


if __name__ == "__main__":
    create_tables()