from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, ForeignKey #importar o criador do banco para conectar e os tipos usados nas colunas
from sqlalchemy.orm import declarative_base, relationship #a base que permite o orm, conecção de classes e objetos com as tabelas sql
from sqlalchemy_utils.types import ChoiceType

db = create_engine('sqlite:///banco.db')
Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column('id', Integer, primary_key= True, autoincrement= True)
    nome = Column('nome', String)
    email = Column('email', String, nullable= False)
    senha = Column('senha', String)
    ativo = Column('ativo', Boolean, default= True)
    admin = Column('admin', Boolean, default= False)

    def __init__(self, nome, email, senha, ativo = True, admin = False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin

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
    itens = relationship("ItenPedido", cascade= 'all, delete')

    def __init__(self, idusuario, status= "PENDENTE", preco= 0):
        self.idusuario = idusuario
        self.status = status
        self.preco = preco

    def atualizar_valor(self):
        self.preco = sum(iten.preco_unitario * iten.quantidade for iten in self.itens)

class ItenPedido(Base):
    __tablename__ = 'itens_pedidos'

    id = Column('id', Integer, primary_key= True, autoincrement= True)
    quantidade = Column('quantidade', Integer)
    sabor = Column('sabor', String)
    tamanho = Column('tamanho', String)
    preco_unitario = Column('preco', Float)
    idpedido = Column('idpedido', ForeignKey('pedidos.id'))

    def __init__(self, quantidade, sabor, tamanho, preco_unitario, idpedido):
        self.quantidade = quantidade
        self.sabor = sabor 
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
        self.idpedido = idpedido

