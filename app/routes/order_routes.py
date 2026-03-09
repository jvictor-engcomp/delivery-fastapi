#importando função que cria um roteador
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import pegar_sessao, verificar_token
from app.schemas.schemas import PedidoSchema, ItemSchema, PedidoSchemaResponse
from app.models.usuario_model import Usuario
from app.models.pedido_model import Pedido
from app.models.itempedido_model import ItemPedido
from typing import List

order_router = APIRouter(prefix= '/orders', tags= ['orders'], dependencies=[Depends(verificar_token)])

#utiliza-se decorator para criar rotas 
@order_router.get('/listarpedidos')
async def listar(usuario: Usuario = Depends(verificar_token), session: Session = Depends(pegar_sessao)):
    '''
    Docstring é captada pelo fastapi, pode ser usada para documentar
    '''
    pedidos = session.query(Pedido).filter(Pedido.id == usuario.id).all()
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
    
@order_router.post('/cancelarpedido/{id_pedido}')
async def cancelar_pedido(id_pedido: int, usuario: Usuario = Depends(verificar_token), session: Session = Depends(pegar_sessao)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(400, 'pedido não encontrado')
    elif pedido.idusuario != usuario.id:
        if not usuario.admin:
            raise HTTPException(401, 'Você não tem permissão para fazer essa modificação')
        
    pedido.status = "CANCELADO"
    session.commit()
    return {
        'mensagem': f'pedido {pedido.id} cancelado',
        'pedido': pedido
    }

@order_router.post('/adicionaritem/{id_pedido}')
async def adicionar_item(id_pedido: int, itemschema: ItemSchema, usuario: Usuario = Depends(verificar_token),  session: Session = Depends(pegar_sessao)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(400, 'Pedido não existe.')
    if  pedido.idusuario != usuario.id and not usuario.admin:
        raise HTTPException(400, 'Você não pode alterar esse pedido.')
    itempedido = ItemPedido(itemschema.quantidade, itemschema.sabor, itemschema.tamanho, itemschema.preco_unitario, itemschema.idpedido)

    session.add(itempedido)
    pedido.atualizar_valor()
    session.commit()

    return {
        'mensagem': f'item {itempedido.id} adicionado.',
        'itempedido': itempedido
    }

@order_router.post('/removeritem/{id_item}')
async def remover_item(id_item: int, usuario: Usuario = Depends(verificar_token),  session: Session = Depends(pegar_sessao)):
    item = session.query(ItemPedido).filter(ItemPedido.id == id_item).first()
    pedido = session.query(Pedido).filter(Pedido.id == item.idpedido).first()
    if not item:
        raise HTTPException(400, 'item não existe.')
    if  pedido.idusuario != usuario.id and not usuario.admin:
        raise HTTPException(400, 'Você não pode remover esse pedido.')
    

    session.delete(item)
    pedido.atualizar_valor()
    session.commit()

    return {
        'mensagem': f'item {item.id} removido do pedido {pedido.id}.',
        'pedido': pedido
    }

@order_router.post('/finalizarpedido/{id_pedido}')
async def finalizar_pedido(id_pedido: int, usuario: Usuario = Depends(verificar_token), session: Session = Depends(pegar_sessao)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(400, 'Pedido não existe.')
    if  pedido.idusuario != usuario.id and not usuario.admin:
        raise HTTPException(400, 'Você não pode alterar esse pedido.')
    
    pedido.status = "FINALIZADO"
    session.commit()

    return {
        'mensagem': f'pedido {pedido.id} cancelado',
        'pedido': pedido
    }

@order_router.get('/visualizarpedido/{id_pedido}', response_model = PedidoSchemaResponse)
async def visualizar_pedido(id_pedido: int, usuario: Usuario = Depends(verificar_token), session: Session = Depends(pegar_sessao)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(400, 'Pedido não existe.')
    if pedido.idusuario != usuario.id and not usuario.admin:
        raise HTTPException(400, 'Você não pode visualizar esse pedido.')
    
    return pedido
    
@order_router.get('/visualizarpedidos/{id_usuario}', response_model = List[PedidoSchemaResponse])
async def visualizar_pedidos(id_usuario: int, usuario: Usuario = Depends(verificar_token), session: Session = Depends(pegar_sessao)):
    pedidos = session.query(Pedido).filter(Pedido.idusuario == id_usuario).all()
    if not pedidos:
        raise HTTPException(400, 'Pedido não existe.')
    if id_usuario != usuario.id and not usuario.admin:
        raise HTTPException(400, 'Você não pode visualizar esse pedido.')
    
    return pedidos
