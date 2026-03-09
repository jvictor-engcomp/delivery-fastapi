from pydantic import BaseModel
from typing import Optional, List

class ItemSchema(BaseModel):
    quantidade: int
    sabor: str 
    tamanho: str
    preco_unitario: float
    idpedido: int

    class Config:
        from_atributes = True 