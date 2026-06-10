from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext


# Chave secreta usada para assinar o token JWT. Em um projeto real, essa chave não deve ficar escrita diretamente no código.
SECRET_KEY = "chave_secreta_raizes_do_nordeste"

# Algoritmo usado para criar e validar o token JWT
ALGORITHM = "HS256"

# Tempo de validade do token em minutos
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Configuração responsável por criptografar e verificar senhas usando bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def gerar_hash_senha(senha: str) -> str:
    """
    Recebe uma senha em texto puro e retorna a senha criptografada.
    Essa senha criptografada é a que será salva no banco.
    """
    return pwd_context.hash(senha)


def verificar_senha(senha_digitada: str, senha_hash: str) -> bool:
    """
    Compara a senha digitada pelo usuário com a senha criptografada salva no banco.
    Retorna True se a senha estiver correta.
    Retorna False se a senha estiver incorreta.
    """
    return pwd_context.verify(senha_digitada, senha_hash)


def criar_token_acesso(dados: dict) -> str:
    """
    Cria um token JWT contendo os dados enviados.
    Normalmente usamos o campo 'sub' para identificar o usuário no token.
    """

    # Cria uma cópia dos dados para não alterar o dicionário original
    dados_para_token = dados.copy()

    # Define quando o token irá expirar
    expiracao = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Adiciona a expiração dentro dos dados do token
    dados_para_token.update({"exp": expiracao})

    # Gera o token JWT assinado com a chave secreta
    token = jwt.encode(dados_para_token, SECRET_KEY, algorithm=ALGORITHM)

    return token


def verificar_token(token: str):
    """
    Verifica se o token JWT é válido.
    Se for válido, retorna os dados que estavam dentro dele.
    Se for inválido, retorna None.
    """

    try:
        # Decodifica o token usando a mesma chave secreta e o mesmo algoritmo
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        return payload

    except JWTError:
        # Se o token for inválido ou expirado, cai aqui
        return None