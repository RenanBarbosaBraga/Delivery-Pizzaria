from fastapi import APIRouter
from sqlalchemy.orm import sessionmaker

from models import Usuario, db

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
async def criar_conta(nome: str, email: str, senha: str):
    Session = sessionmaker(bind=db)
    session = Session()
    usuario = session.query(Usuario).filter_by(email=email).first()
    if usuario:
        return {"mensagem": "Já existe um usuário com esse email"}
    else:
        novo_usuario = Usuario(nome, email, senha)
        session.add(novo_usuario)
        session.commit()
        return {"mensagem": "Usuario cadastrado com sucesso"}
