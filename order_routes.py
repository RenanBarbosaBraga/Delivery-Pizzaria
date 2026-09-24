from fastapi import APIRouter

order_routes = APIRouter(prefix="/orders", tags=["order"])


@order_routes.get("/")
async def pedidos():
    """
    Essa é a rota padrão de pedidos do nosso sistema
    """
    return {"mensagem": "Você acessou a rota de pedidos"}
