from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.connection import Base

class ItemAddon(Base):
    __tablename__ = 'itensaddons '

    id = Column('id', Integer, primary_key= True, autoincrement= True)
    idaddon = Column('idaddon', Integer, ForeignKey('addons.id'))
    iditempedido = Column('iditempedido', Integer, ForeignKey('itens_pedidos.id'))

    addon = relationship('Addon')
    itempedido = relationship('ItemPedido', back_populates= 'itemaddons')

    def __init__(self, idaddon, iditempedido, ):
        self.idaddon = idaddon
        self.iditempedido = iditempedido