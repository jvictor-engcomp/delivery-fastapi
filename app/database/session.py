from sqlalchemy.orm import sessionmaker
from app.database.connection import db

SessionLocal = sessionmaker(bind= db)