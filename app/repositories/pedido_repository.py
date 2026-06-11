from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.item_pedido_model import ItemPedido
from app.models.pedido_model import Pedido
from app.schemas.pedido_schema import PedidoCreate
from app.repositories.produto_repository import buscar_produto_por_id


# Lista todos os pedidos cadastrados.
def listar_pedidos(db: Session, canalPedido: str | None = None):
    query = db.query(Pedido)

    if canalPedido:
        query = query.filter(Pedido.canalPedido == canalPedido)

    return query.all()

# Busca um pedido pelo id.
def buscar_pedido_por_id(db: Session, pedido_id: int):
    return db.query(Pedido).filter(Pedido.id == pedido_id).first()


# Cria um novo pedido com seus itens.
def criar_pedido(db: Session, pedido: PedidoCreate):
    # Variável que acumula o valor total do pedido.
    valor_total = Decimal("0.00")

    # Criamos primeiro o pedido principal com status PENDENTE.
    novo_pedido = Pedido(
        cliente_id=pedido.cliente_id,
        canalPedido=pedido.canalPedido.value,
        status="PENDENTE",
        valor_total=valor_total
    )

    # Adiciona o pedido à sessão.
    db.add(novo_pedido)

    # Faz um flush para gerar o id do pedido antes do commit. Precisamos desse id para cadastrar os itens do pedido.
    db.flush()

    # Percorre cada item enviado no pedido.
    for item in pedido.itens:
        # Busca o produto no banco pelo id informado.
        produto = buscar_produto_por_id(db, item.produto_id)

        # Se o produto não existir, desfaz a operação e lança erro.
        if produto is None:
            db.rollback()
            raise ValueError(f"Produto com id {item.produto_id} não encontrado.")

        # Verifica se há estoque suficiente.
        if produto.estoque < item.quantidade:
            db.rollback()
            raise ValueError(f"Estoque insuficiente para o produto {produto.nome}.")

        # Calcula o subtotal do item.
        subtotal_item = produto.preco * item.quantidade

        # Soma o subtotal ao valor total do pedido.
        valor_total += subtotal_item

        # Cria o item do pedido.
        novo_item = ItemPedido(
            pedido_id=novo_pedido.id,
            produto_id=produto.id,
            quantidade=item.quantidade,
            preco_unitario=produto.preco
        )

        # Adiciona o item à sessão.
        db.add(novo_item)

        # Atualiza o estoque do produto.
        produto.estoque = produto.estoque - item.quantidade

    # Atualiza o valor total do pedido depois de calcular todos os itens.
    novo_pedido.valor_total = valor_total

    db.commit()

    db.refresh(novo_pedido)

    return novo_pedido


# Atualiza o status de um pedido. Será usado quando o pagamento for aprovado.
def atualizar_status_pedido(db: Session, pedido: Pedido, novo_status: str):
    # Altera o status do pedido.
    pedido.status = novo_status

    db.commit()

    db.refresh(pedido)

    return pedido