from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import verificar_token, pegar_sessao
from typing import List

from app.models.usuario_model import Usuario

from app.schemas.usuario_schema import UsuarioSchemaResponse
from app.schemas.usuario_schema import AtualizarUsuarioSchema

user_router = APIRouter(prefix= '/user', tags=['user'])

@user_router.get('/me', response_model= UsuarioSchemaResponse)
async def info(usuario: Usuario = Depends(verificar_token)):
    """Retorna informações do usuário logado no momento."""
    
    return usuario

@user_router.put('/me')
async def atualizar_usuario(novosdados: AtualizarUsuarioSchema, usuario: Usuario = Depends(verificar_token), session: Session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.id == usuario.id).first()
    usuario.nome = novosdados.nome
    session.commit()

    return {
        'mensagem': 'Nome alterado com sucesso!'
    }

@user_router.delete('/me')
async def desativar_usuario(usuario: Usuario = Depends(verificar_token), session: Session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.id == usuario.id).first()
    usuario.ativo = False
    session.commit()

    return {
        'mensagem': 'Usuario desativad com sucesso!'
    }

@user_router.get('/admin', response_model= List[UsuarioSchemaResponse])
async def visualizar_todos_usuarios(usuario: Usuario = Depends(verificar_token), session: Session = Depends(pegar_sessao)):
    if not usuario.admin:
        raise HTTPException(403, 'Você não tem permissão para essa rota.')
    
    usuarios = session.query(Usuario).all()
    return usuarios

@user_router.get('admin/{idusuario}', response_model= UsuarioSchemaResponse)
async def visualizar_usuario_específico(idusuario: int, usuario: Usuario = Depends(verificar_token), session: Session = Depends(pegar_sessao)):
    if not usuario.admin:
        raise HTTPException(403, 'Você não tem permissão para essa rota.')
    
    usuario = session.query(Usuario).filter(Usuario.id == idusuario).first()
    return usuario

@user_router.put('/admin/{idusuario}')
async def atualizar_usuario(idusuario: int, novosdados: AtualizarUsuarioSchema, usuario: Usuario = Depends(verificar_token), session: Session = Depends(pegar_sessao)):
    if not usuario.admin:
        raise HTTPException(403, 'Você não tem permissão para essa rota.')

    usuario = session.query(Usuario).filter(Usuario.id == idusuario).first()
    usuario.nome = novosdados.nome
    session.commit()

    return {
        'mensagem': 'Nome alterado com sucesso!'
    }