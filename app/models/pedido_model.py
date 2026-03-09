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
    preco = Column('preco', Float)
    itens = relationship("ItemPedido", cascade= 'all, delete')

    def __init__(self, idusuario, status= "PENDENTE", preco= 0):
        self.idusuario = idusuario
        self.status = status
        self.preco = preco

    def atualizar_valor(self):
        self.preco = sum(iten.preco_unitario * iten.quantidade for iten in self.itens)