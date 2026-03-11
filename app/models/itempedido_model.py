from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database.connection import Base

class ItemPedido(Base):
    __tablename__ = 'itens_pedidos'

    id = Column('id', Integer, primary_key= True, autoincrement= True)
    idprodutovariante = Column('idprodutovariante', Integer, ForeignKey('produtosvariantes.id'))
    quantidade = Column('quantidade', Integer)
    preco_item = Column('preco', Float)
    idpedido = Column('idpedido', ForeignKey('pedidos.id'))

    produtovariante = relationship("ProdutoVariante")

    def __init__(self, idprodutovariante, quantidade, idpedido, preco_item = 0,):
        self.idprodutovariante = idprodutovariante
        self.quantidade = quantidade
        self.preco_item = preco_item
        self.idpedido = idpedido

    def atualizar_valor_item(self):
        self.preco_item = self.produtovariante.preco_variante * self.quantidade