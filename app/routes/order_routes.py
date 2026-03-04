#importando função que cria um roteador
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import pegar_sessao
from app.schemas.schemas import PedidoSchema
from app.models.models import Pedido, Usuario 

order_router = APIRouter(prefix= '/order', tags= ['order'])

#utiliza-se decorator para criar rotas 
@order_router.get('/listar')
async def listar():
    '''
    Docstring é captada pelo fastapi, pode ser usada para documentar
    '''
    return {'mensagem': 'listando pedidos'}

@order_router.post('/criarpedido')
async def criar_pedido(pedidoschema: PedidoSchema, session: Session = Depends(pegar_sessao)):
    usuario_referente = session.query(Usuario).filter(Usuario.id == pedidoschema.idusuario).first()
    if usuario_referente:
        novo_pedido = Pedido(pedidoschema.idusuario)
        session.add(novo_pedido)
        session.commit()
        return{'mensagem': 'pedido criado'}
    else: 
        raise HTTPException(400, 'usuario nao existe')

