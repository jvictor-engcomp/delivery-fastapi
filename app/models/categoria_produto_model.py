from sqlalchemy import Column, Integer, String
from app.database.connection import Base

class CategoriaProduto(Base):
    __tablename__ = 'categoriaprodutos'
    
    id = Column('id', Integer, primary_key= True, autoincrement= True)
    nome = Column('nome', String)

    def __init__(self, nome):
        self.nome = nome