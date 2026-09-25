from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencies import pegar_sessao
from main import bcrypt_context
from models import Usuario
from schemas import UsuarioSchema

auth_routes = APIRouter(prefix="/auth", tags=["auth"])


@auth_routes.get("/")
async def autenticar():
    """
    Essa é a rota padrão de autenticação do nosso sistema, todas as rotas dos pedidos precisam de autentifcação
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
