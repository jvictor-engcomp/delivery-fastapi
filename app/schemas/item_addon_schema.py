from pydantic import BaseModel

class ItemAddonSchema(BaseModel):
    idaddon: int
    iditempedido: int

    class Config:
        from_attributes = True 