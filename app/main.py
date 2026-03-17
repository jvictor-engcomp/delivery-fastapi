#criando uma instância e jogando ela para a variável app
from fastapi import FastAPI
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))

app = FastAPI()

bcrypt_context = CryptContext(schemes= ['argon2'], deprecated= "auto")
oauth2_schema = OAuth2PasswordBearer(tokenUrl='auth/login-form')

from app.routes.auth_routes import auth_router
from app.routes.order_routes import order_router
from app.routes.menu_routes import menu_router
from app.routes.user_routes import user_router

#roteadores incluidos no app
app.include_router(auth_router)
app.include_router(order_router)
app.include_router(menu_router)
app.include_router(user_router)



#para rodar no terminal para criar um servidor: uvicorn main:app --reload