from pydantic import BaseModel
from typing import Optional, List

class LoginSchema(BaseModel):
    email: str
    senha: str

    class Config:
        from_atributes = True 