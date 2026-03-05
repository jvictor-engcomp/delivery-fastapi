#importando função que cria um roteador
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import pegar_sessao, verificar_token
from app.schemas.schemas import PedidoSchema
from app.models.models import Pedido, Usuario 

order_router = APIRouter(prefix= '/order', tags= ['order'], dependencies=[Depends(verificar_token)])

#utiliza-se decorator para criar rotas 
@order_router.get('/listar')
async def listar(session: Session = Depends(pegar_sessao)):
    '''
    Docstring é captada pelo fastapi, pode ser usada para documentar
    '''
    pedidos = session.query(Pedido).all
    return {'mensagem': 'listando pedidos',
            'pedidos': pedidos}

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
    
@order_router.post('/excluir-pedido/{id_pedido}')
async def exluir_pedido(id_pedido: int, usuario: Usuario = Depends(verificar_token), session: Session = Depends(pegar_sessao)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(400, 'pedido não encontrado')
    elif pedido.idusuario != usuario.id:
        if not usuario.admin:
            raise HTTPException(400, 'Você não tem permissão para fazer essa modificação')
        
    pedido.status = "CANCELADO"
    session.commit()
    return {
        'mensagem': f'pedido {pedido.id} cancelado',
        'pedido': pedido
    }
