# Este arquivo permite que a pasta repositories seja reconhecida como um pacote Python.

from app.repositories.usuario_repository import (
    buscar_cliente_por_email,
    buscar_cliente_por_id,
    criar_cliente,
    listar_clientes,
)

from app.repositories.pagamento_repository import (
    buscar_pagamento_por_id,
    criar_pagamento,
    listar_pagamentos,
)

from app.repositories.pedido_repository import (
    atualizar_status_pedido,
    buscar_pedido_por_id,
    criar_pedido,
    listar_pedidos,
)

from app.repositories.produto_repository import (
    atualizar_estoque_produto,
    buscar_produto_por_id,
    criar_produto,
    listar_produtos,
)