# Este arquivo permite importar os schemas de forma mais organizada em outras partes do projeto.

from app.schemas.usuario_schema import ClienteCreate, ClienteResponse
from app.schemas.item_pedido_schema import ItemPedidoCreate, ItemPedidoResponse
from app.schemas.pagamento_schema import PagamentoCreate, PagamentoResponse
from app.schemas.pedido_schema import PedidoCreate, PedidoResponse
from app.schemas.produto_schema import ProdutoCreate, ProdutoResponse