from pydantic import BaseModel, EmailStr


class LoginSchema(BaseModel):
    # Email informado pelo usuário no momento do login
    email: EmailStr

    # Senha digitada pelo usuário no momento do login
    senha: str


class TokenSchema(BaseModel):
    # Token JWT gerado pelo sistema após o login
    access_token: str

    # Tipo do token. O padrão usado em APIs é "bearer"
    token_type: str