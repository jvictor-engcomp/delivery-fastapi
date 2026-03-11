from pydantic import BaseModel

class ProdutoVarianteSchema(BaseModel):
    idproduto: int
    variacao: str
    preco_variante: float

    class Config:
        from_atributes = True