from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database.connection import Base

class Pedido(Base):
    __tablename__ = 'pedidos'

    # Status_Pedidos = {
    #     ('PENDENDTE', 'PENDENTE'),
    #     ('CANCELADO', 'CANCELADO'),
    #     ('FINALIZADO', 'FINALIZADO')
    # }

    id = Column('id', Integer, primary_key= True, autoincrement= True)
    idusuario = Column('idusuario', ForeignKey('usuarios.id'))
    
    status = Column('status', String, default= 'PENDENTE')
    preco_pedido = Column('preco', Float)

    itens = relationship("ItemPedido", back_populates= 'pedido')
    
    def __init__(self, idusuario, status= "PENDENTE", preco_pedido = 0):
        self.idusuario = idusuario
        self.status = status
        self.preco_pedido = preco_pedido

    def atualizar_valor(self):
        self.preco_pedido = sum(item.preco_item for item in self.itens) 