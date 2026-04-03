from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = 'xptNK0KibjiTvzaScWizVPPvNI42qsMybcCxz5Nb1Nr'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

bcrypt_context = CryptContext(schemes= ['argon2'], deprecated= "auto")
oauth2_schema = OAuth2PasswordBearer(tokenUrl='auth/login-form')
