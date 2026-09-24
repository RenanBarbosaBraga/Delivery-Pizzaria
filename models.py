from sqlalchemy import (
    Boolean,
    Column,
    Float,
    ForeignKey,
    Integer,
    String,
    create_engine,
)
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils.types import ChoiceType

db = create_engine("sqlite:///database/banco.db")

Base = declarative_base()


class Usuario(Base):
    _tablename_ = "usuarios"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String)
    email = Column("email", String, nullable=False)
    senha = Column("senha", String, nullable=False)
    ativo = Column("ativo", Boolean)
    admin = Column("admin", Boolean, default=False)

    def __init__(self, nome, email, senha, ativo=True, admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin


class Pedido(Base):
    _tablename_ = "pedidos"

    STATUS_PEDIDOS = (
        ("PENDENTE", "PENDENTE"),
        ("CANCELADO", "CANCELADO"),
        ("FINALIZADO", "FINALIZADO"),
    )

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    status = Column(
        "status", String, ChoiceType(choices=STATUS_PEDIDOS)
    )  # pendente, cancelado e finalizado
    usuario = Column("usuario", ForeignKey("usuarios.id"))
    preco = Column("preco", Float)

    def __init__(self, usuario, status="PENDENTE", preco=0):
        self.status = status
        self.usuario = usuario
        self.preco = preco


class ItemPedido(Base):
    _tablename_ = "itens_pedido"

    TAMANHOS_PIZZA = (("P", "P"), ("M", "M"), ("G", "G"), ("GG", "GG"))

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    quantidade = Column("quantidade", Integer)
    sabor = Column("sabor", String)
    tamanho = Column("tamanho", String, ChoiceType(choices=TAMANHOS_PIZZA))
    preco_unitario = Column("preco_unitario", Float)
    pedido = Column("pedido", ForeignKey("pedidos.id"))

    def __init__(self, quantidade, sabor, tamanho, preco_unitario, pedido):
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
        self.pedido = pedido
