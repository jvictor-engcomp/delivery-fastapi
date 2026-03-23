from sqlalchemy import create_engine #importar o criador do banco para conectar e os tipos usados nas colunas
from sqlalchemy.orm import declarative_base #a base que permite o orm, conecção de classes e objetos com as tabelas sql

import os

DATABASE_URL = os.getenv("DATABASE_URL")

db = create_engine(DATABASE_URL)

Base = declarative_base()