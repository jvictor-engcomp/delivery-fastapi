#importando função que cria um roteador
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import pegar_sessao, verificar_token
from app.schemas.pedido_schema import PedidoSchema
from app.schemas.itempedido_schema import ItemSchema
from app.schemas.pedido_schema import PedidoSchemaResponse
from app.models.usuario_model import Usuario
from app.models.pedido_model import Pedido
from app.models.itempedido_model import ItemPedido
from typing import List

order_router = APIRouter(prefix= '/orders', tags= ['orders'], dependencies=[Depends(verificar_token)])

#utiliza-se decorator para criar rotas 
@order_router.get('/')
async def listar(usuario: Usuario = Depends(verificar_token), session: Session = Depends(pegar_sessao)):
    '''
    Docstring é captada pelo fastapi, pode ser usada para documentar
    '''
    pedidos = session.query(Pedido).filter(Pedido.idusuario == usuario.id).all()
    return {'mensagem': 'listando pedidos',
            'pedidos': pedidos}

@order_router.post('/')
async def criar_pedido(pedidoschema: PedidoSchema, session: Session = Depends(pegar_sessao)):
    usuario_referente = session.query(Usuario).filter(Usuario.id == pedidoschema.idusuario).first()
    if usuario_referente:
        novo_pedido = Pedido(pedidoschema.idusuario)
        session.add(novo_pedido)
        session.commit()
        return{'mensagem': 'pedido criado'}
    else: 
        raise HTTPException(404, 'usuario nao existe')
    
@order_router.delete('/{id_pedido}/status')
async def cancelar_pedido(id_pedido: int, usuario: Usuario = Depends(verificar_token), session: Session = Depends(pegar_sessao)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(404, 'Pedido não encontrado.')
    elif pedido.idusuario != usuario.id:
        if not usuario.admin:
            raise HTTPException(403, 'Você não tem permissão para fazer essa modificação')
        
    pedido.status = "CANCELADO"
    session.commit()
    return {
        'mensagem': f'pedido {pedido.id} cancelado',
        'pedido': pedido
    }

@order_router.patch('/{id_pedido}/status')
async def finalizar_pedido(id_pedido: int, usuario: Usuario = Depends(verificar_token), session: Session = Depends(pegar_sessao)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(404, 'Pedido não existe.')
    if  pedido.idusuario != usuario.id and not usuario.admin:
        raise HTTPException(403, 'Você não pode alterar esse pedido.')
    
    pedido.status = "FINALIZADO"
    session.commit()

    return {
        'mensagem': f'pedido {pedido.id} cancelado',
        'pedido': pedido
    }

@order_router.get('/{id_pedido}', response_model = PedidoSchemaResponse)
async def visualizar_pedido(id_pedido: int, usuario: Usuario = Depends(verificar_token), session: Session = Depends(pegar_sessao)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(404, 'Pedido não existe.')
    if pedido.idusuario != usuario.id and not usuario.admin:
        raise HTTPException(403, 'Você não pode visualizar esse pedido.')
    
    return pedido
    
@order_router.get('/admin/{id_usuario}', response_model = List[PedidoSchemaResponse])
async def visualizar_pedidos(id_usuario: int, usuario: Usuario = Depends(verificar_token), session: Session = Depends(pegar_sessao)):
    pedidos = session.query(Pedido).filter(Pedido.idusuario == id_usuario).all()
    if not pedidos:
        raise HTTPException(404, 'Pedido não existe.')
    if id_usuario != usuario.id and not usuario.admin:
        raise HTTPException(403, 'Você não pode visualizar esse pedido.')
    
    return pedidos

@order_router.post('/{id_pedido}/itens')
async def adicionar_item(id_pedido: int, itemschema: ItemSchema, usuario: Usuario = Depends(verificar_token),  session: Session = Depends(pegar_sessao)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(404, 'Pedido não existe.')
    if  pedido.idusuario != usuario.id and not usuario.admin:
        raise HTTPException(403, 'Você não pode alterar esse pedido.')
    itempedido = ItemPedido(itemschema.quantidade, itemschema.sabor, itemschema.tamanho, itemschema.preco_unitario, itemschema.idpedido)

    session.add(itempedido)
    pedido.atualizar_valor()
    session.commit()

    return {
        'mensagem': f'item {itempedido.id} adicionado.',
        'itempedido': itempedido
    }

@order_router.delete('/{id_pedido}/itens/{id_item}')
async def remover_item(id_pedido: int, id_item: int, usuario: Usuario = Depends(verificar_token),  session: Session = Depends(pegar_sessao)):
    item = session.query(ItemPedido).filter(ItemPedido.id == id_item).first()
    if not item:
        raise HTTPException(404, 'item não existe.')
    if item.idpedido != id_pedido:
        raise HTTPException(400, 'Pedido e item não têm relação.')
    
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if  pedido.idusuario != usuario.id and not usuario.admin:
        raise HTTPException(403, 'Você não pode remover esse pedido.')
    

    session.delete(item)
    pedido.atualizar_valor()
    session.commit()

    return {
        'mensagem': f'item {item.id} removido do pedido {pedido.id}.',
        'pedido': pedido
    }


