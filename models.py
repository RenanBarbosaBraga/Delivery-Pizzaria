from sqlalchemy import Boolean, Column, Float, Integer, String, base, create_engine
from sqlalchemy.orm import declarative_base

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
