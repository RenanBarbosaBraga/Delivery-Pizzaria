from calendar import month
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from dependencies import pegar_sessao
from main import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY, bcrypt_context
from models import Usuario
from schemas import LoginSchema, UsuarioSchema

auth_routes = APIRouter(prefix="/auth", tags=["auth"])


def criar_token(id_usuario, token_time=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    expiration_date = datetime.now(timezone.utc) + token_time
    token = {"sub": id_usuario, "exp": expiration_date}
    encoded_jwt = jwt.encode(token, SECRET_KEY, ALGORITHM)  # type: ignore
    return encoded_jwt


def verificar_token(token, session: Session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter_by(id=1).first()
    return usuario


def autenticar_usuario(email: str, senha: str, session: Session):
    usuario = session.query(Usuario).filter_by(email=email).first()
    if not usuario:
        return False
    if not bcrypt_context.verify(senha, usuario.senha):
        return False
    return usuario


@auth_routes.get("/")
async def autenticar():
    """
    Essa é a rota padrão de autenticação do nosso sistema, todas as rotas dos pedidos precisam de autentificação
    """
    return {
        "mensagem": "Você acessou a rota padrão de autenticação",
        "autentificado": False,
    }


@auth_routes.post("/criar_conta")
async def criar_conta(
    usuario_schema: UsuarioSchema, session: Session = Depends(pegar_sessao)
):
    usuario = session.query(Usuario).filter_by(email=usuario_schema.email).first()
    if usuario:
        raise HTTPException(status_code=400, detail="E-mail do usuario ja cadastrado")
    else:
        senha_criptografada = bcrypt_context.hash(usuario_schema.senha)
        novo_usuario = Usuario(
            usuario_schema.nome, usuario_schema.email, senha_criptografada
        )
        session.add(novo_usuario)
        session.commit()
        return {"mensagem": f"Usuario cadastrado com sucesso {usuario_schema.email}"}


@auth_routes.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(pegar_sessao)):  # noqa: B008
    usuario = session.query(Usuario).filter_by(email=login_schema.email).first()
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuario não encontrado")
    access_token = criar_token(usuario.id)
    refresh_token = criar_token(usuario.id, token_time=timedelta(days=7))
    return {"access_token": access_token, "token_type": "Bearer"}


@auth_routes.get("/refresh")
async def use_refresh_token(token, session: Session = Depends(pegar_sessao)):
    usuario = verificar_token(token, session)
    access_token = criar_token(id_usuario=usuario.id)
    return {"access_token": access_token, "token_type": "Bearer"}
