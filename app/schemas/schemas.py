from pydantic import BaseModel
from typing import Optional

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
        