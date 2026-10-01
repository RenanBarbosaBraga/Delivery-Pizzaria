from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencies import pegar_sessao, verificar_token
from models import Pedido
from schemas import PedidoSchema

order_routes = APIRouter(
    prefix="/orders", tags=["order"], dependencies=[Depends(verificar_token)]
)


@order_routes.get("/")
async def pedidos():
    """
    Essa é a rota padrão de pedidos do nosso sistema
    """
    return {"mensagem": "Você acessou a rota de pedidos"}


@order_routes.post("/pedido")
async def criar_pedido(
    pedido_schema: PedidoSchema,
    session: Session = Depends(pegar_sessao),  # noqa: B008
):
    novo_pedido = Pedido(usuario=pedido_schema.usuario)
    session.add(novo_pedido)
    session.commit()
    return {"mensagem": f"Pedido criado com sucesso. ID do pedido {novo_pedido.id}"}


@order_routes.post("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao)):
    pedido = session.query(Pedido).filter_by(id=id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    pedido.status = "CANCELADO"
    return {
        "mensagem": f"Pedido de id: n°{id_pedido} cancelado com sucesso",
        "pedido": pedido,
    }
