from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.connection import Base

class Produto(Base):
    __tablename__ = 'produtos'

    id = Column('id', Integer, primary_key= True, autoincrement= True)
    nome = Column('nome', String)
    idcategoria = Column('idcategoria', Integer, ForeignKey('categoriaprodutos.id'))

    categoria = relationship('CategoriaProduto')
    variantes = relationship('ProdutoVariante', cascade='all, delete')

    def __init__(self, nome, idcategoria):
        self.nome = nome
        self.idcategoria = idcategoria