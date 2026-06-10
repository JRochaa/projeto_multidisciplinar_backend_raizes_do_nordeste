# API Raízes do Nordeste

API desenvolvida para o Projeto Multidisciplinar do curso de Análise e Desenvolvimento de Sistemas.

O projeto simula o back-end de uma rede chamada **Raízes do Nordeste**, com funcionalidades de cadastro de usuários/clientes, produtos, autenticação JWT, criação de pedidos e processamento de pagamento mock.

## Tecnologias utilizadas

* FastAPI
* PostgreSQL
* Python
* SQLAlchemy
* Pydantic
* JWT
* Uvicorn

## Funcionalidades

* Cadastro de usuários/clientes
* Login com autenticação JWT
* Cadastro de produtos
* Listagem de produtos
* Criação de pedidos
* Inclusão de itens no pedido
* Cálculo automático do valor total do pedido
* Baixa automática no estoque
* Pagamento mock
* Atualização automática do status do pedido para `PAGO`
* Validação de erros de negócio

## Estrutura principal do projeto

```text
PROJETO_BACKEND_RAIZESDONORDESTE/
├── app/
│   ├── core/
│   │   └── config.py
│   ├── database/
│   │   └── connection.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── item_pedido_model.py
│   │   ├── pagamento_model.py
│   │   ├── pedido_model.py
│   │   ├── produto_model.py
│   │   └── usuario_model.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── pagamento_repository.py
│   │   ├── pedido_repository.py
│   │   ├── produto_repository.py
│   │   └── usuario_repository.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth_routes.py
│   │   ├── pagamento_routes.py
│   │   ├── pedido_routes.py
│   │   ├── produto_routes.py
│   │   └── usuario_routes.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth_schema.py
│   │   ├── item_pedido_schema.py
│   │   ├── pagamento_schema.py
│   │   ├── pedido_schema.py
│   │   ├── produto_schema.py
│   │   └── usuario_schema.py
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── pagamento_service.py
│   │   └── pedido_service.py
│   └── main.py
├── .env
├── create_tables.py
├── README.md
└── requirements.txt
```

## Configuração do ambiente

Clone o repositório e acesse a pasta do projeto:

```bash
git clone <https://github.com/JRochaa/projeto_multidisciplinar_backend_raizes_do_nordeste>
cd <nome-da-pasta-do-projeto>
```

Crie e ative o ambiente virtual:

```bash
python -m venv venv
```

No Windows:

```bash
venv\Scripts\activate
```

No Linux ou macOS:

```bash
source venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Configuração do banco de dados

O projeto utiliza PostgreSQL.

Crie um banco de dados no PostgreSQL/pgAdmin e configure o arquivo `.env` com os dados de conexão.

Neste repositório já existe um arquivo chamado `.env.example` com a estrutura necessária. Para configurar o projeto, copie esse arquivo ou renomeie para `.env`.

Depois, substitua as informações da variável `DATABASE_URL` pelos dados do seu PostgreSQL.As partes que devem ser substituídas são:

usuario: usuário do PostgreSQL
senha: senha do PostgreSQL
nome_do_banco_de_dados: nome do banco de dados criado no pgAdmin

Exemplo:

```env
DATABASE_URL=postgresql://usuario:senha@localhost:5432/nome_do_banco_de_dados
```

## Criação das tabelas

O projeto possui um arquivo separado para criação das tabelas:

```bash
python create_tables.py
```

Esse comando cria as tabelas com base nos models definidos no projeto.

O arquivo `app/models/__init__.py` centraliza os imports dos models, permitindo que o SQLAlchemy reconheça as tabelas corretamente.

## Como rodar a API

Execute o servidor com:

```bash
uvicorn app.main:app --reload
```

Depois acesse:

```text
http://127.0.0.1:8000
```

A documentação automática do Swagger fica disponível em:

```text
http://127.0.0.1:8000/docs
```

## Fluxo principal da aplicação

O fluxo principal da API é:

```text
Usuário/Cliente → Produto → Pedido → Pagamento → Status PAGO
```

## Endpoints principais

### Autenticação

| Método | Endpoint                  | Descrição                           |
| ------ | ------------------------- | ----------------------------------- |
| POST   |      `/auth/login`        | Realiza login e retorna o token JWT |

### Usuários/Clientes

| Método | Endpoint                 | Descrição                        |
| ------ | ------------------------ | -------------------------------- |
| POST   | `/usuarios/`             | Cadastra um novo usuário/cliente |
| GET    | `/usuarios/`             | Lista usuários/clientes          |
| GET    | `/usuarios/{cliente_id}` | Busca usuário/cliente por ID     |

### Produtos

| Método | Endpoint                 | Descrição                |
| ------ | ------------------------ | ------------------------ |
| POST   | `/produtos/`             | Cadastra um novo produto |
| GET    | `/produtos/`             | Lista produtos           |
| GET    | `/produtos/{produto_id}` | Busca produto por ID     |

### Pedidos

| Método | Endpoint               | Descrição           |
| ------ | ---------------------- | ------------------- |
| POST   | `/pedidos/`            | Cria um novo pedido |
| GET    | `/pedidos/`            | Lista pedidos       |
| GET    | `/pedidos/{pedido_id}` | Busca pedido por ID |

### Pagamentos

| Método | Endpoint                     | Descrição                  |
| ------ | ---------------------------- | -------------------------- |
| POST   | `/pagamentos/`               | Processa um pagamento mock |
| GET    | `/pagamentos/`               | Lista pagamentos           |
| GET    | `/pagamentos/{pagamento_id}` | Busca pagamento por ID     |

## Exemplo de uso

### 1. Cadastrar usuário/cliente

```json
{
  "nome": "Jadson Rocha",
  "email": "jadson@email.com",
  "telefone": "11999999999",
  "endereco": "São Paulo - SP",
  "senha": "123456"
}
```

### 2. Realizar login

Exemplo de dados:

```text
username: jadson@email.com
password: 123456
```

Resposta esperada:

```json
{
  "access_token": "token_jwt_gerado",
  "token_type": "bearer"
}
```

### 3. Cadastrar produto

```json
{
  "nome": "Cuscuz Nordestino",
  "descricao": "Produto típico do Nordeste",
  "preco": 12.90,
  "estoque": 10
}
```

### 4. Criar pedido

```json
{
  "cliente_id": 2,
  "itens": [
    {
      "produto_id": 1,
      "quantidade": 2
    }
  ]
}
```

Resposta esperada:

```json
{
  "id": 2,
  "cliente_id": 2,
  "status": "PENDENTE",
  "valor_total": "25.80",
  "itens": [
    {
      "id": 1,
      "pedido_id": 2,
      "produto_id": 1,
      "quantidade": 2,
      "preco_unitario": "12.90"
    }
  ]
}
```

### 5. Processar pagamento mock

```json
{
  "pedido_id": 2,
  "metodo": "PIX"
}
```

Resposta esperada:

```json
{
  "id": 1,
  "pedido_id": 2,
  "metodo": "PIX",
  "status": "APROVADO",
  "valor": "25.80"
}
```

### 6. Conferir status do pedido

Após o pagamento, ao buscar o pedido novamente, o status deverá estar como:

```json
{
  "id": 2,
  "cliente_id": 2,
  "status": "PAGO",
  "valor_total": "25.80",
  "itens": [
    {
      "id": 1,
      "pedido_id": 2,
      "produto_id": 1,
      "quantidade": 2,
      "preco_unitario": "12.90"
    }
  ]
}
```

## Regras de negócio implementadas

* Um pedido deve possuir pelo menos um item.
* O sistema verifica se o produto existe antes de criar o pedido.
* O sistema verifica se há estoque suficiente antes de criar o pedido.
* O valor total do pedido é calculado automaticamente.
* O estoque do produto é reduzido após a criação do pedido.
* O pagamento mock é aprovado automaticamente.
* Após o pagamento aprovado, o pedido recebe o status `PAGO`.
* Um pedido já pago não pode ser pago novamente.
* Um pagamento não pode ser feito para um pedido inexistente.

## Testes de erro validados

Durante os testes, foram validadas as seguintes situações:

| Situação                                     | Resultado esperado |
| -------------------------------------------- | ------------------ |
| Tentar pagar pedido já pago                  | `400 Bad Request`  |
| Tentar criar pedido com estoque insuficiente | `400 Bad Request`  |
| Tentar pagar pedido inexistente              | `400 Bad Request`  |

## Documentação Swagger

A API possui documentação automática gerada pelo FastAPI.

Após iniciar o servidor, acesse:

```text
http://127.0.0.1:8000/docs
```

No Swagger é possível testar todas as rotas da API, incluindo cadastro, login, produtos, pedidos e pagamentos.

## Status do projeto

Etapas concluídas:

* Requisitos
* DER
* Endpoints da API
* Estrutura do projeto
* Banco de dados
* Login JWT
* Pedido e pagamento mock
* Swagger e README

