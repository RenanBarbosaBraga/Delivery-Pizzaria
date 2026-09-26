from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies import pegar_sessao
from models import Pedido
from schemas import PedidoSchema

order_routes = APIRouter(prefix="/orders", tags=["order"])


@order_routes.get("/")
async def pedidos():
    """
    Essa é a rota padrão de pedidos do nosso sistema
    """
    return {"mensagem": "Você acessou a rota de pedidos"}


@order_routes.post("/pedido")
async def criar_pedido(
    pedido_schema: PedidoSchema, session: Session = Depends(pegar_sessao)
):
    novo_pedido = Pedido(usuario=pedido_schema.usuario)
    session.add(novo_pedido)
    session.commit()
    return {"mensagem": f"Peido criado com sucesso. ID do pedido {novo_pedido.id}"}
