from pydantic import BaseModel

class AddonSchema(BaseModel):
    idcategoria: int
    nome: str
    preco_addon: float

    class Config:
        from_atributes = True 