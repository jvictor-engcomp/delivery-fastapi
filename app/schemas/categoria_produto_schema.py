from pydantic import BaseModel

class CategoriaProdutoSchema(BaseModel):
    nome: str

    class Config:
        from_atributes = True 