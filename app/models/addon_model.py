from sqlalchemy import Column, Integer, Float, String, ForeignKey
from app.database.connection import Base

class Addon(Base):
    __tablename__ = 'addons'

    id = Column('id', Integer, primary_key= True, autoincrement= True)
    idcategoria = Column('idcategora', Integer, ForeignKey('categoriaaddons.id'))
    idpedido = Column('idpedido', Integer, ForeignKey('pedidos.id'))
    nome = Column('nome', String)
    preco_addon = Column('preco_addon', Float)

    def __init__(self, idpedido, idcategoria, nome, preco_addon):
        self.idpedido = idpedido
        self.idcategoria = idcategoria
        self.nome = nome
        self.preco_addon = preco_addon