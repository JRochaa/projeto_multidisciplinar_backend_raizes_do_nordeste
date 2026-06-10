from fastapi import FastAPI

from app.routes import auth_routes
from app.routes import usuario_routes
from app.routes import produto_routes
from app.routes import pedido_routes
from app.routes import pagamento_routes

app = FastAPI(
    title="API Raízes do Nordeste",
    description="""
API desenvolvida para o Projeto Multidisciplinar de Análise e Desenvolvimento de Sistemas.

A aplicação simula o back-end da rede Raízes do Nordeste, permitindo:

- Cadastro e autenticação de usuários/clientes
- Cadastro e consulta de produtos
- Criação de pedidos com itens
- Processamento de pagamento mock
- Atualização automática do status do pedido após pagamento
""",
    version="1.0.0"
)



#Incluindo as rotas na aplicção
app.include_router(auth_routes.router)
app.include_router(usuario_routes.router) 
app.include_router(produto_routes.router)
app.include_router(pedido_routes.router)
app.include_router(pagamento_routes.router)

# Rota inicial usada apenas para verificar se a API está funcionando.
@app.get("/")
def home():
    return {"message": "API Raízes do Nordeste funcionando"}