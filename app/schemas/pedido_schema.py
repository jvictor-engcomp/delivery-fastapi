from pydantic import BaseModel
from typing import Optional, List
from app.schemas.itempedido_schema import ItemSchema

class PedidoSchema(BaseModel):
    idusuario: int

    class Config:
        from_attributes = True

class PedidoSchemaResponse(BaseModel):
    id: int
    idusuario: int
    status: str
    preco_pedido: float
    itens: List[ItemSchema]

    class Config:
        from_attributes = True