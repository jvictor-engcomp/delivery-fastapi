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

class UsuarioSchemaResponse(BaseModel):
    id: int
    nome: str
    email: str

    class Config:
        from_atributes = True

class AtualizarUsuarioSchema(BaseModel):
    nome: str