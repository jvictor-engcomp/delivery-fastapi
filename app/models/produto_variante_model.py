from sqlalchemy import Column, Integer, Float, String, ForeignKey
from app.database.connection import Base

class ProdutoVariante(Base):
    __tablename__ = 'produtosvariantes'

    id = Column('id', Integer, primary_key= True, autoincrement= True)
    idproduto = Column('idproduto', Integer, ForeignKey('produtos.id'))
    variacao = Column('variacao', String)
    preco_variante = Column('preco_variante', Float)

    def __init__(self, idproduto, variacao, preco_variante):
        self.idproduto = idproduto
        self.variacao = variacao
        self.preco_variante = preco_variante
    
