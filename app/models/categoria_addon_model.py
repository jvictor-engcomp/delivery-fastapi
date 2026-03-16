from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.connection import Base

class CategoriaAddon(Base):
    __tablename__ = 'categoriaaddons'

    id = Column('id', Integer, primary_key= True, autoincrement= True)
    nome = Column('nome', String)
    
    addons = relationship('Addon', back_populates= 'categoria')

    def __init__(self, nome):
        self.nome = nome