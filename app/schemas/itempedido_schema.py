from pydantic import BaseModel
from typing import Optional, List
from app.schemas.produto_variante_schema import ProdutoVarianteSchema
from app.schemas.item_addon_schema import ItemAddonSchema


class ItemSchema(BaseModel):
    idprodutovariante: int
    quantidade: int
    idpedido: int 

    class Config:
        from_atributes = True 