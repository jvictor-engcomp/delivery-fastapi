from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database.connection import Base

class ItemPedido(Base):
    __tablename__ = 'itens_pedidos'

    id = Column('id', Integer, primary_key= True, autoincrement= True)
    idpedido = Column('idpedido', ForeignKey('pedidos.id'))
    idprodutovariante = Column('idprodutovariante', Integer, ForeignKey('produtosvariantes.id'))

    quantidade = Column('quantidade', Integer)
    preco_item = Column('preco', Float)
    
    pedido = relationship('Pedido', back_populates= 'itens')
    produtovariante = relationship("ProdutoVariante")
    itemaddons = relationship('ItemAddon', back_populates= 'itempedido')

    def atualizar_valor_item(self):
        soma_addons = sum(itemaddon.addon.preco_addon for itemaddon in self.itemaddons)
        self.preco_item = (self.produtovariante.preco_variante + soma_addons) * self.quantidade
    
    def __init__(self, idprodutovariante, quantidade, idpedido, preco_item =0):
        self.idprodutovariante = idprodutovariante
        self.quantidade = quantidade
        self.preco_item = preco_item
        self.idpedido = idpedido
