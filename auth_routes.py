from fastapi import APIRouter

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
