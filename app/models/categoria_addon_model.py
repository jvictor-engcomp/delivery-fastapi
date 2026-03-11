from sqlalchemy import Column, Integer, String
from app.database.connection import Base

class CategoriaAddon(Base):
    __tablename__ = 'categoriaaddons'

    id = Column('id', Integer, primary_key= True, autoincrement= True)
    nome = Column('nome', String)
    
    def __init__(self, nome):
        self.nome = nome