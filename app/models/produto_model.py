from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.connection import Base

class Produto(Base):
    __tablename__ = 'produtos'

    id = Column('id', Integer, primary_key= True, autoincrement= True)
    nome = Column('nome', String)
    idcategoria = Column('idcategoria', Integer, ForeignKey('categoriaprodutos.id'))

    def __init__(self, nome, idcategoria):
        self.nome = nome
        self.idcategoria = idcategoria