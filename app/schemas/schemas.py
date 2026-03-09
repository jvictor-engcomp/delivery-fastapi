from pydantic import BaseModel
from typing import Optional, List

class UsuarioSchema(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: Optional[bool]
    admin: Optional[bool]

    #vai ser interpretado como orm 
    class Config:
        from_atributes = True

class PedidoSchema(BaseModel):
    idusuario: int

    class Config:
        from_atributes = True


class LoginSchema(BaseModel):
    email: str
    senha: str

    class Config:
        from_atributes = True 

class ItemSchema(BaseModel):
    quantidade: int
    sabor: str 
    tamanho: str
    preco_unitario: float
    idpedido: int

    class Config:
        from_atributes = True 
        
class PedidoSchemaResponse(BaseModel):
    id: int
    idusuario: int
    status: str
    preco: float
    itens: List[ItemSchema]

    class Config:
        from_atributes = True