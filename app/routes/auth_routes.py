from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.database.connection import get_db
from app.repositories.usuario_repository import buscar_cliente_por_email
from app.schemas.auth_schema import LoginSchema, TokenSchema
from app.services.auth_service import criar_token_acesso, verificar_senha, verificar_token


# Cria o conjunto de rotas relacionadas à autenticação
router = APIRouter(
    prefix="/auth",
    tags=["Autenticação"]
)

# Configuração usada pelo Swagger para permitir autenticação com Bearer Token.
# tokenUrl indica qual rota gera o token.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.post("/login", response_model=TokenSchema)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Realiza o login do cliente usando o padrão OAuth2.
    O Swagger usa os campos username e password.
    No nosso caso, o username será o email do cliente.
    """

    # O Swagger envia o email no campo username
    email = form_data.username

    # O Swagger envia a senha no campo password
    senha = form_data.password

    # Busca o cliente pelo email informado
    cliente = buscar_cliente_por_email(db, email)

    # Se não encontrar o cliente, retorna erro
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha inválidos."
        )

    # Verifica se a senha digitada confere com a senha criptografada no banco
    senha_valida = verificar_senha(senha, cliente.senha)

    # Se a senha estiver errada, retorna erro
    if not senha_valida:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha inválidos."
        )

    # Cria o token JWT usando o email como identificação
    access_token = criar_token_acesso(
        dados={"sub": cliente.email}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


def obter_cliente_logado(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    Valida o token JWT enviado na requisição.
    Se o token for válido, busca e retorna o cliente logado.
    Se o token for inválido, retorna erro 401.
    """

    # Decodifica e valida o token JWT
    payload = verificar_token(token)

    # Se o token for inválido ou expirado, payload será None
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado."
        )

    # Pega o email salvo dentro do token. No login, salvamos o email dentro do campo "sub".
    email = payload.get("sub")

    # Se não existir email no token, retorna erro
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido."
        )

    # Busca o cliente no banco pelo email vindo do token
    cliente = buscar_cliente_por_email(db, email)

    # Se o cliente não existir mais no banco, retorna erro
    if cliente is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado."
        )

    return cliente

@router.get("/me")
def dados_usuario_logado(cliente_logado = Depends(obter_cliente_logado)):
    """
    Rota protegida.
    Só pode ser acessada se o usuário enviar um token JWT válido.
    Retorna os dados do usuário/cliente autenticado.
    """

    return {
        "id": cliente_logado.id,
        "nome": cliente_logado.nome,
        "email": cliente_logado.email,
        "telefone": cliente_logado.telefone,
        "endereco": cliente_logado.endereco
    }