from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.connection import Base

class Addon(Base):
    __tablename__ = 'addons'

    id = Column('id', Integer, primary_key= True, autoincrement= True)
    idcategoria = Column('idcategora', Integer, ForeignKey('categoriaaddons.id'))
    nome = Column('nome', String)
    preco_addon = Column('preco_addon', Float)

    categoria = relationship("CategoriaAddon", back_populates= 'addons')

    def __init__(self, idcategoria, nome, preco_addon):
        self.idcategoria = idcategoria
        self.nome = nome
        self.preco_addon = preco_addon