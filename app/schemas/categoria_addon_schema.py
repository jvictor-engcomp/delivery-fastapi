from pydantic import BaseModel

class CategoriaAddonSchema(BaseModel):
    nome: str

    class Config:
        from_atributes = True 