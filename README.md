# API Raízes do Nordeste

Repositório do projeto:

```text
https://github.com/JRochaa/projeto_multidisciplinar_backend_raizes_do_nordeste
```

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
* Perfis de usuário: `CLIENTE` e `ADMINISTRADOR`
* Controle de acesso por perfil em rotas administrativas
* Cadastro e consulta de produtos
* Criação de pedidos com itens
* Registro do canal de origem do pedido por meio do campo `canalPedido`
* Filtro de pedidos por canal de origem
* Cálculo automático do valor total do pedido
* Baixa automática no estoque
* Pagamento mock com possibilidade de aprovação ou recusa
* Atualização automática do status do pedido para `PAGO` quando o pagamento é aprovado
* Manutenção do pedido como `PENDENTE` quando o pagamento é recusado
* Validação de regras de negócio e permissões

## Perfis de usuário e permissões

O sistema possui dois perfis principais:

| Perfil          | Permissões principais                                                                                      |
| --------------- | ---------------------------------------------------------------------------------------------------------- |
| `CLIENTE`       | Pode fazer login, consultar seus próprios dados, criar pedidos para si mesmo e pagar seus próprios pedidos |
| `ADMINISTRADOR` | Pode cadastrar produtos, listar usuários, listar pedidos, filtrar pedidos por canal e listar pagamentos    |

Usuários cadastrados pela rota pública de cadastro são criados automaticamente com o perfil `CLIENTE`.

Para criar um usuário administrador em ambiente local, cadastre o usuário normalmente e depois altere o perfil no banco de dados:

```sql
UPDATE clientes
SET perfil = 'ADMINISTRADOR'
WHERE email = 'admin@email.com';
```

## Multicanalidade do pedido

A API registra o canal de origem do pedido por meio do campo `canalPedido`.

Valores aceitos:

* `APP`
* `TOTEM`
* `BALCAO`
* `PICKUP`
* `WEB`

Exemplo de criação de pedido:

```json
{
  "cliente_id": 1,
  "canalPedido": "APP",
  "itens": [
    {
      "produto_id": 1,
      "quantidade": 2
    }
  ]
}
```

Também é possível filtrar pedidos por canal:

```text
GET /pedidos/?canalPedido=APP
```

Essa funcionalidade permite rastrear a origem dos pedidos e atender ao requisito de multicanalidade do domínio.

## Pagamento mock

O pagamento mock simula o comportamento de um serviço externo de pagamento.

A regra implementada utiliza uma probabilidade aproximada de:

* 66,7% para pagamento `APROVADO`
* 33,3% para pagamento `RECUSADO`

Quando o pagamento é aprovado, o pedido tem seu status atualizado para:

```text
PAGO
```

Quando o pagamento é recusado, o pedido permanece com status:

```text
PENDENTE
```

Nesse caso, a API retorna uma mensagem informando que o pagamento foi recusado e que o pedido pode ser pago novamente.

Exemplo de resposta com pagamento aprovado:

```json
{
  "id": 1,
  "pedido_id": 1,
  "metodo": "PIX",
  "status": "APROVADO",
  "valor": "25.80",
  "mensagem": "Pagamento aprovado com sucesso."
}
```

Exemplo de resposta com pagamento recusado:

```json
{
  "id": 2,
  "pedido_id": 2,
  "metodo": "PIX",
  "status": "RECUSADO",
  "valor": "25.80",
  "mensagem": "Pagamento recusado. O pedido permanece pendente e pode ser pago novamente."
}
```

## Coleção Postman

A coleção Postman com os testes da API está disponível em:

```text
postman/API_Raizes_do_Nordeste_Postman_Collection_Atualizada.json
```

Para executar os testes:

1. Importe a coleção no Postman.
2. Inicie a API localmente:

```bash
uvicorn app.main:app --reload
```

3. Configure a variável `base_url` como:

```text
http://127.0.0.1:8000
```

4. Crie ou confirme um usuário administrador no banco.
5. Execute as requisições na ordem apresentada na coleção.

A coleção contempla cenários positivos e negativos, incluindo autenticação, permissões por perfil, criação de pedidos com `canalPedido`, filtro por canal, estoque insuficiente, pagamento mock e tentativa de acesso indevido a recursos de outro cliente.


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
├── postman/
│   └── API_Raizes_do_Nordeste_Postman_Collection_Atualizada.json
├── .env.example
├── .gitignore
├── create_tables.py
├── README.md
└── requirements.txt
```

## Configuração do ambiente

Clone o repositório e acesse a pasta do projeto:

```bash
git clone https://github.com/JRochaa/projeto_multidisciplinar_backend_raizes_do_nordeste
cd projeto_multidisciplinar_backend_raizes_do_nordeste
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

Depois, substitua as informações da variável `DATABASE_URL` pelos dados do seu PostgreSQL.

As partes que devem ser substituídas são:

* `usuario`: usuário do PostgreSQL
* `senha`: senha do PostgreSQL
* `nome_do_banco_de_dados`: nome do banco de dados criado no pgAdmin

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
Usuário/Cliente → Produto → Pedido → Pagamento Mock
```

Quando o pagamento mock é aprovado, o pedido tem o status atualizado para:

```text
PAGO
```

Quando o pagamento mock é recusado, o pedido permanece com o status:

```text
PENDENTE
```

Assim, o cliente pode tentar realizar o pagamento novamente.


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

Usuários cadastrados por essa rota são criados com o perfil `CLIENTE`.

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

Essa operação exige usuário autenticado com perfil `ADMINISTRADOR`.

```json
{
  "nome": "Cuscuz Nordestino",
  "descricao": "Produto típico do Nordeste",
  "preco": 12.90,
  "estoque": 10
}
```

### 4. Criar pedido

Essa operação exige usuário autenticado. O cliente só pode criar pedido para si mesmo.

```json
{
  "cliente_id": 2,
  "canalPedido": "APP",
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
  "canalPedido": "APP",
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

Resposta esperada para pagamento aprovado:

```json
{
  "id": 1,
  "pedido_id": 2,
  "metodo": "PIX",
  "status": "APROVADO",
  "valor": "25.80",
  "mensagem": "Pagamento aprovado com sucesso."
}
```

Resposta esperada para pagamento recusado:

```json
{
  "id": 2,
  "pedido_id": 2,
  "metodo": "PIX",
  "status": "RECUSADO",
  "valor": "25.80",
  "mensagem": "Pagamento recusado. O pedido permanece pendente e pode ser pago novamente."
}
```

### 6. Conferir status do pedido

Após o pagamento aprovado, ao buscar o pedido novamente, o status deverá estar como `PAGO`.

Caso o pagamento seja recusado, o pedido continuará como `PENDENTE`.


## Regras de negócio implementadas

* Um pedido deve possuir pelo menos um item.
* A criação de pedido exige o campo `canalPedido`.
* O campo `canalPedido` aceita apenas os valores `APP`, `TOTEM`, `BALCAO`, `PICKUP` e `WEB`.
* A API permite filtrar pedidos por canal de origem.
* O sistema verifica se o produto existe antes de criar o pedido.
* O sistema verifica se há estoque suficiente antes de criar o pedido.
* O valor total do pedido é calculado automaticamente.
* O estoque do produto é reduzido após a criação do pedido.
* O pagamento mock pode ser aprovado ou recusado.
* A probabilidade aproximada do pagamento mock é de 66,7% para `APROVADO` e 33,3% para `RECUSADO`.
* Após o pagamento aprovado, o pedido recebe o status `PAGO`.
* Após o pagamento recusado, o pedido permanece com o status `PENDENTE`.
* Um pedido já pago não pode ser pago novamente.
* Um pagamento não pode ser feito para um pedido inexistente.
* Um cliente não pode pagar pedido pertencente a outro cliente.
* Apenas usuários com perfil `ADMINISTRADOR` podem acessar rotas administrativas, como cadastro de produtos, listagem de usuários, listagem de pedidos e listagem de pagamentos.

## Testes de erro validados

Durante os testes, foram validadas as seguintes situações:

| Situação                                     | Resultado esperado         |
| -------------------------------------------- | -------------------------- |
| Acessar rota protegida sem token             | `401 Unauthorized`         |
| Cliente tentar cadastrar produto             | `403 Forbidden`            |
| Cliente tentar listar todos os pedidos       | `403 Forbidden`            |
| Cliente tentar pagar pedido de outro cliente | `403 Forbidden`            |
| Criar pedido sem `canalPedido`               | `422 Unprocessable Entity` |
| Criar pedido com `canalPedido` inválido      | `422 Unprocessable Entity` |
| Criar pedido com estoque insuficiente        | `400 Bad Request`          |
| Tentar pagar pedido já pago                  | `400 Bad Request`          |
| Tentar pagar pedido inexistente              | `400 Bad Request`          |



