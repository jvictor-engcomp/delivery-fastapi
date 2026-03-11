from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.connection import Base

class CategoriaProduto(Base):
    __tablename__ = 'categoriaprodutos'
    
    id = Column('id', Integer, primary_key= True, autoincrement= True)
    nome = Column('nome', String)

    pedidos =  relationship('Produto', cascade='all, delete')
    
    def __init__(self, nome):
        self.nome = nome