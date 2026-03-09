from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.database.connection import Base

class ItemPedido(Base):
    __tablename__ = 'itens_pedidos'

    id = Column('id', Integer, primary_key= True, autoincrement= True)
    quantidade = Column('quantidade', Integer)
    sabor = Column('sabor', String)
    tamanho = Column('tamanho', String)
    preco_unitario = Column('preco', Float)
    idpedido = Column('idpedido', ForeignKey('pedidos.id'))

    def __init__(self, quantidade, sabor, tamanho, preco_unitario, idpedido):
        self.quantidade = quantidade
        self.sabor = sabor 
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
        self.idpedido = idpedido