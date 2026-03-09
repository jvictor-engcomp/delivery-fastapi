#importando função que cria um roteador
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.models.usuario_model import Usuario  
from app.dependencies import pegar_sessao, verificar_token
from app.main import bcrypt_context, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from app.schemas.schemas import UsuarioSchema, LoginSchema, UsuarioSchemaResponse
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

def criar_token(idusuario, tempo_expiracao= timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)):
    data_expiracao = datetime.now(timezone.utc) + tempo_expiracao
    dict_info = {'sub': str(idusuario), "exp": data_expiracao}
    token = jwt.encode(dict_info, key= SECRET_KEY, algorithm= ALGORITHM)

    return token

def autenticar_usuario(email, senha, session):
    usuario = session.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        return False
    elif not bcrypt_context.verify(senha, usuario.senha):
        return False
    return usuario

auth_router = APIRouter(prefix= '/auth', tags= ['auth'])

#utiliza-se decorator para criar rotas 
@auth_router.get('/me', response_model= UsuarioSchemaResponse)
async def info(usuario: Usuario = Depends(verificar_token)):
    return usuario

@auth_router.post('/registrar')
async def registrar_usuario(usuarioschema: UsuarioSchema, session: Session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email == usuarioschema.email).first()
    if usuario:
        raise HTTPException(400, detail='usuario já cadastrado')
    else:
        senha_criptografada = bcrypt_context.hash(usuarioschema.senha)
        novo_usuario = Usuario(usuarioschema.nome, usuarioschema.email, senha_criptografada, usuarioschema.ativo, usuarioschema.admin)
        session.add(novo_usuario)
        session.commit()
        return {'mensagem': 'Usuario criado com sucesso'} 
    
@auth_router.post('/login')
async def login(loginschema: LoginSchema, session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(loginschema.email, loginschema.senha, session)
    if not usuario:
        raise HTTPException(400, 'email ou senha errados')
    else:
        access_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, tempo_expiracao= timedelta(days= 7))
        return {'access_token': access_token, 
                'refresh_token': refresh_token,
                'token_type': 'Bearer'}
    
@auth_router.post('/login-form')
async def login_form(dados_form: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(pegar_sessao)):
    """
        Rota criada apenas para permitir uso do botão Authorize da documentação do FastApi
    """
    usuario = autenticar_usuario(dados_form.username, dados_form.password, session)
    if not usuario:
        raise HTTPException(400, 'email ou senha errados')
    else:
        access_token = criar_token(usuario.id)
        return {'access_token': access_token,
                'token_type': 'Bearer'}

@auth_router.get('/refresh')
async def use_refresh_token(usuario: Usuario = Depends(verificar_token)):
    access_token = criar_token(usuario.id)
    return {'access_token': access_token, 
                'token_type': 'Bearer'}