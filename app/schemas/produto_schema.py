from pydantic import BaseModel

class ProdutoSchema(BaseModel):
    nome: str
    idcategoria: int

    class Config:
        from_attributes = True 