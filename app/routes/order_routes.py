#importando função que cria um roteador
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import pegar_sessao, verificar_token
from typing import List

from app.models.usuario_model import Usuario
from app.models.pedido_model import Pedido
from app.models.itempedido_model import ItemPedido
from app.models.itemaddon_model import ItemAddon

from app.schemas.pedido_schema import PedidoSchema
from app.schemas.pedido_schema import PedidoSchemaResponse
from app.schemas.itempedido_schema import ItemSchema
from app.schemas.item_addon_schema import ItemAddonSchema

order_router = APIRouter(prefix= '/orders', tags= ['orders'], dependencies=[Depends(verificar_token)])

@order_router.post('/')
async def criar_pedido(pedidoschema: PedidoSchema, session: Session = Depends(pegar_sessao)):
    """Primeiro passo, criar um pedido que abriga itens"""
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
    """Apenas muda o status do pedido"""
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


@order_router.get('/')
async def listar(usuario: Usuario = Depends(verificar_token), session: Session = Depends(pegar_sessao)):
    """Lista pedidos do usuário logado no momento"""
    pedidos = session.query(Pedido).filter(Pedido.idusuario == usuario.id).all()
    return {'mensagem': 'listando pedidos',
            'pedidos': pedidos}

    
@order_router.patch('/{id_pedido}/status')
async def finalizar_pedido(id_pedido: int, usuario: Usuario = Depends(verificar_token), session: Session = Depends(pegar_sessao)):
    """Muda apenas o status"""
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
    """Permite ver o seu pedido. Caso usuário logado seja admin, esse pode ver qualquer pedido"""
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(404, 'Pedido não existe.')
    if pedido.idusuario != usuario.id and not usuario.admin:
        raise HTTPException(403, 'Você não pode visualizar esse pedido.')
    
    return pedido
    
@order_router.get('/admin/{id_usuario}', response_model = List[PedidoSchemaResponse])
async def visualizar_pedidos(id_usuario: int, usuario: Usuario = Depends(verificar_token), session: Session = Depends(pegar_sessao)):
    """Rota pensada no admin, ele pode listar os pedidos de qualquer usuário"""
    pedidos = session.query(Pedido).filter(Pedido.idusuario == id_usuario).all()
    if not pedidos:
        raise HTTPException(404, 'Pedido não existe.')
    if id_usuario != usuario.id and not usuario.admin:
        raise HTTPException(403, 'Você não pode visualizar esses pedidos.')
    
    return pedidos

@order_router.post('/{id_pedido}/itens')
async def adicionar_item(id_pedido: int, itemschema: ItemSchema, usuario: Usuario = Depends(verificar_token),  session: Session = Depends(pegar_sessao)):
    """Essa rota cria um ItemPedido e o adiciona em um pedido"""
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(404, 'Pedido não existe.')
    if  pedido.idusuario != usuario.id and not usuario.admin:
        raise HTTPException(403, 'Você não pode alterar esse pedido.')
    itempedido = ItemPedido(itemschema.idprodutovariante, itemschema.quantidade, itemschema.idpedido)

    session.add(itempedido)
    session.commit()
    itempedido.atualizar_valor_item()
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

@order_router.post('/pedido/{iditem}/addon')
async def adicionar_item_addon(iditem: int, itemaddonschema: ItemAddonSchema, usuario: Usuario = Depends(verificar_token),  session: Session = Depends(pegar_sessao)):
    """Essa rota cria um ItemAddon e o adiciona em um ItemPedido"""
    item = session.query(ItemPedido).filter(ItemPedido.id == iditem).first()
    if not item:
        raise HTTPException(404, 'Item não existe.')
    if  item.pedido.idusuario != usuario.id and not usuario.admin:
        raise HTTPException(403, 'Você não pode alterar esse item.')
    itemaddon = ItemAddon(itemaddonschema.idaddon, itemaddonschema.iditempedido)

    session.add(itemaddon)
    item.atualizar_valor_item()
    item.pedido.atualizar_valor()
    session.commit()

    return {
        'mensagem': f'Addon {itemaddon.id} adicionado.',
        'itemaddon': itemaddon
    }

@order_router.delete('/pedido/{id_item}/addon/{id_addon}')
async def remover_item(id_item: int, id_addon: int, usuario: Usuario = Depends(verificar_token),  session: Session = Depends(pegar_sessao)):
    item_addon = session.query(ItemAddon).filter(ItemAddon.id == id_addon).first()
    if not item_addon:
        raise HTTPException(404, 'Addon não existe.')
    if item_addon.iditempedido != id_item:
        raise HTTPException(400, 'Addon e item não têm relação.')
    
    item_pedido = session.query(ItemPedido).filter(ItemPedido.id == id_item).first()

    if  item_pedido.pedido.idusuario != usuario.id and not usuario.admin:
        raise HTTPException(403, 'Você não pode remover esse pedido.')
    

    session.delete(item_addon)
    session.commit()
    item_pedido.atualizar_valor_item()
    item_pedido.pedido.atualizar_valor()
    session.commit()

    return {
        'mensagem': f'Addon {item_addon.id} removido do item {item_pedido.id}.',
        'item pedido': item_pedido
    }